texture gTexture;
sampler LiverySampler = sampler_state { Texture=<gTexture>; MinFilter=Linear; MagFilter=Linear; MipFilter=Linear; };
float4 livery(float2 uv:TEXCOORD0):COLOR0 { return tex2D(LiverySampler,uv); }
technique SAFGLivery { pass P0 { AlphaBlendEnable=TRUE; SrcBlend=SRCALPHA; DestBlend=INVSRCALPHA; ZWriteEnable=FALSE; DepthBias=-0.0002; PixelShader=compile ps_2_0 livery(); } }
