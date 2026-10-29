"""Validate public data and build the private SAFGworldShaders asset catalog.

Never executes public scripts. Only fixed-schema JSON, reviewed FX and PNG/DDS
bytes are imported. Organization bases are deliberately excluded.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import warnings
import xml.etree.ElementTree as ET
from PIL import Image

REPOSITORY = 'InfinityPR/SAFG-World'
KEY = re.compile(r'[a-z0-9][a-z0-9_-]{0,63}\Z')
TEXTURE = re.compile(r'[A-Za-z0-9_.*?-]{1,64}\Z')
UNIFORM = re.compile(r'[A-Za-z_][A-Za-z0-9_]{0,63}\Z')
HEX = re.compile(r'[0-9a-f]{40}\Z')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def data_file(folder, name, suffixes, maximum):
    require(isinstance(name,str) and re.fullmatch(r'[a-zA-Z0-9_-]+\.[a-zA-Z0-9]+',name), 'Asset filenames must be plain local filenames')
    file=folder/name
    require(file.suffix in suffixes and not file.is_symlink() and file.is_file(), 'Missing or unsupported asset: '+name)
    require(0<file.stat().st_size<=maximum,'Asset size limit exceeded: '+name)
    return file.read_bytes()


def read_release(folder):
    require(not folder.is_symlink() and KEY.fullmatch(folder.name),'Invalid release folder')
    source=data_file(folder,'request.json',{'.json'},16384)
    spec=json.loads(source)
    require(isinstance(spec,dict) and set(spec)<= {'model','target','kind','github','textures','fx','image','uniform'},'Unknown submission fields')
    target=spec.get('target');kind=spec.get('kind');model=spec.get('model')
    require(target in ('vehicle','skin') and kind in ('livery','effect'),'Choose vehicle/skin and livery/effect')
    require(type(model) is int and (400<=model<=611 if target=='vehicle' else 0<=model<=312),'Invalid GTA model')
    require(isinstance(spec.get('github'),str) and re.fullmatch(r'https://github\.com/InfinityPR/SAFG-World/pull/[1-9][0-9]*',spec['github']),'Use the submission PR URL from SAFG-World')
    textures=spec.get('textures')
    require(isinstance(textures,list) and 1<=len(textures)<=8 and all(isinstance(v,str) for v in textures) and len(set(textures))==len(textures),'Use 1-8 distinct target textures')
    require(all(isinstance(v,str) and TEXTURE.fullmatch(v) and v!='*' for v in textures),'Invalid texture target; a lone wildcard is forbidden')
    require(spec.get('uniform') is None or isinstance(spec['uniform'],str) and UNIFORM.fullmatch(spec['uniform']),'Invalid texture uniform')
    fx=data_file(folder,spec.get('fx'),{'.fx'},131072)
    require(b'\x00' not in fx,'FX must be text')
    fx.decode('utf-8')
    files={spec['fx']:fx}
    release={key:spec[key] for key in ('model','target','kind','github','textures')}
    release.update(integrated=True,fx={'path':'assets/'+folder.name+'/'+spec['fx'],'sha256':hashlib.sha256(fx).hexdigest()})
    if spec.get('uniform'):release['uniform']=spec['uniform']
    if spec.get('image'):
        image=data_file(folder,spec['image'],{'.png','.dds'},4*1024*1024)
        with warnings.catch_warnings():
            warnings.simplefilter('error',Image.DecompressionBombWarning)
            with Image.open(folder/spec['image']) as decoded:
                require(decoded.format in ('PNG','DDS'),'Only PNG/DDS textures are allowed')
                width,height=decoded.size
                require(1<=width<=1024 and 1<=height<=1024,'Textures must be at most 1024x1024')
                decoded.load()
        files[spec['image']]=image
        release['image']={'path':'assets/'+folder.name+'/'+spec['image'],'sha256':hashlib.sha256(image).hexdigest(),'width':width,'height':height}
    require(kind!='livery' or 'image' in release,'Liveries require a texture')
    fingerprint=hashlib.sha256(json.dumps(release,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return release,files,fingerprint


def validate(world):
    world=Path(world)
    root=world/'shaders'
    require(root.is_dir() and not root.is_symlink(),'Missing shaders directory')
    result={};total=0
    for folder in sorted(root.iterdir()):
        if folder.name=='README.md':continue
        require(folder.is_dir() and not folder.is_symlink(),'Only release folders belong under shaders')
        release,files,fingerprint=read_release(folder)
        result[folder.name]=(release,files,fingerprint)
        total+=sum(map(len,files.values()))
    require(len(result)<=256 and total<=64*1024*1024,'Catalog exceeds 256 releases or 64 MiB')
    return result


def lua(value):
    if value is True:return 'true'
    if value is False:return 'false'
    if isinstance(value,str):
        # All exported strings have already passed the ASCII path/schema checks.
        require(value.isascii(),'Generated Lua strings must be ASCII')
        return json.dumps(value)
    if type(value) is int:return str(value)
    if isinstance(value,list):return '{'+','.join(lua(v) for v in value)+'}'
    if isinstance(value,dict):return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in value.items())+'}'
    raise ValueError('Unsupported catalog value')


def github(path):
    return json.loads(subprocess.check_output(['gh','api','repos/'+REPOSITORY+'/'+path],text=True))


def verify_merge(world,key,release,files):
    number=release['github'].rsplit('/',1)[1]
    pull=github('pulls/'+number)
    require(pull.get('merged') is True and pull.get('merged_by',{}).get('login')=='InfinityPR'
        and pull.get('base',{}).get('ref')=='main'
        and pull.get('base',{}).get('repo',{}).get('full_name')==REPOSITORY,
        'Shader PR must be merged into SAFG-World main by InfinityPR: '+key)
    require(type(pull.get('changed_files'))is int and pull['changed_files']<=100,'Submit at most 100 changed files per PR')
    records=github('pulls/'+number+'/files?per_page=100')
    require(isinstance(records,list),'PR file inventory is unavailable')
    approved={record['filename']:record.get('sha') for record in records if record.get('status')in ('added','modified')}
    expected={'request.json':(world/'shaders'/key/'request.json').read_bytes(),**files}
    for name,content in expected.items():
        blob=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        require(approved.get('shaders/'+key+'/'+name)==blob,'Merged PR does not contain these exact asset bytes: '+key+'/'+name)


def publish(world,resource,verify_github=False):
    world=Path(world).resolve();resource=Path(resource).resolve()
    releases=validate(world)
    statefile=resource/'world-catalog.json'
    previous=json.loads(statefile.read_text()) if statefile.exists() else {}
    require(set(previous)<=set(releases),'Merged releases cannot be deleted; existing approvals must remain usable')
    catalog={};state={};assets={}
    # Complete validation and immutable-key checks before changing any output.
    for key,(release,files,fingerprint) in releases.items():
        old=previous.get(key)
        require(not old or old['fingerprint']==fingerprint,'Release keys are immutable; submit a new key/version: '+key)
        if old:commit=old['commit']
        else:
            if verify_github:verify_merge(world,key,release,files)
            paths=['shaders/'+key+'/request.json']+['shaders/'+key+'/'+name for name in files]
            commit=subprocess.check_output(['git','-C',str(world),'log','-1','--format=%H','--',*paths],text=True).strip()
        require(HEX.fullmatch(commit),'The release assets must be committed to Git')
        release['commit']=commit;catalog[key]=release;state[key]={'fingerprint':fingerprint,'commit':commit}
        for name,content in files.items():assets['assets/'+key+'/'+name]=content
    meta=ET.parse(resource/'meta.xml')
    for node in list(meta.getroot().findall('file')):
        if any((node.get('src')or '').startswith('assets/'+key+'/') for key in set(previous)|set(catalog)):meta.getroot().remove(node)
    for asset in sorted(assets):ET.SubElement(meta.getroot(),'file',{'src':asset})
    for name,content in assets.items():
        destination=resource/name
        require(not destination.is_symlink() and not any(p.is_symlink() for p in destination.parents if p!=resource.parent),'Output cannot contain symlinks')
        destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(content)
    (resource/'releases.lua').write_text('-- Generated from reviewed SAFG-World submissions. Do not edit by hand.\nSAFGShaderReleases='+lua(catalog)+'\n')
    statefile.write_text(json.dumps(state,sort_keys=True,indent=2)+'\n')
    ET.indent(meta,space=' ');meta.write(resource/'meta.xml',encoding='unicode')
    print('Validated and imported',len(catalog),'shader releases; organization bases were not imported.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--world',type=Path,required=True);parser.add_argument('--resource',type=Path);parser.add_argument('--verify-github',action='store_true')
    args=parser.parse_args()
    try:
        if args.resource:publish(args.world,args.resource,args.verify_github)
        else:print('Validated',len(validate(args.world)),'shader submissions.')
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError,subprocess.CalledProcessError) as error:
        raise SystemExit('SAFG World validation failed: '+str(error))
