/* Generative motion scenes rendered with WebGL. Used to render the background video loops.
   window.SCENE(canvas, mode) starts a scene; window.renderAt(seconds) draws one exact frame for video capture. */
(function () {
  var FRAG = {
    /* Liquid marble: domain-warped noise in emerald, porcelain and brass */
    marble: [
      'vec3 pal(float t){vec3 a=vec3(.93,.91,.87),b=vec3(.12,.30,.24),c=vec3(.66,.53,.35);',
      'vec3 col=mix(a,b,smoothstep(.15,.75,t));col=mix(col,c,smoothstep(.62,.7,t)*(1.-smoothstep(.7,.8,t))*.9);return col;}',
      'vec3 scene(vec2 p,float T){p*=1.6;vec2 q=vec2(fbm(p+.06*T),fbm(p+vec2(5.2,1.3)-.05*T));',
      'vec2 r=vec2(fbm(p+3.*q+vec2(1.7,9.2)+.08*T),fbm(p+3.*q+vec2(8.3,2.8)-.07*T));float f=fbm(p+3.5*r);',
      'vec3 col=pal(f);float vein=smoothstep(.02,0.,abs(f-.58))*.55;col=mix(col,vec3(.80,.66,.43),vein);return col;}'
    ].join('\n'),
    /* Silk: layered satin folds in midnight navy with champagne highlights */
    silk: [
      'float hf(vec2 p,float T){p+=.45*vec2(sin(p.y*1.3+T*.20),sin(p.x*1.1-T*.17));',
      'return sin(p.x*2.2+p.y*.8+T*.30)*.55+sin(p.x*1.1-p.y*1.7-T*.22)*.35+sin(p.x*3.7+p.y*2.3+T*.18)*.12;}',
      'vec3 scene(vec2 p,float T){vec2 q=p*2.4;float e=.01;float c0=hf(q,T);',
      'vec3 nrm=normalize(vec3(-(hf(q+vec2(e,0.),T)-c0)/e,-(hf(q+vec2(0.,e),T)-c0)/e,1.4));',
      'vec3 L=normalize(vec3(-.5,.6,.65));vec3 H=normalize(L+vec3(0,0,1));',
      'float dif=max(dot(nrm,L),0.);float spc=pow(max(dot(nrm,H),0.),38.);float rim=pow(1.-nrm.z,1.5);',
      'vec3 navy=vec3(.035,.07,.13),blue=vec3(.16,.25,.40),gold=vec3(.93,.82,.60);',
      'vec3 col=mix(navy,blue,dif*dif)+gold*spc*.85+blue*rim*.4;',
      'col*=1.-.4*smoothstep(.5,1.3,length(p*vec2(.8,1.)));return col;}'
    ].join('\n'),
    /* Light through blinds: soft sunlight bars drifting across warm stone */
    stone: [
      'vec3 scene(vec2 p,float T){vec3 stone=vec3(.83,.80,.76),shade=vec3(.60,.56,.51),warm=vec3(.97,.86,.72);',
      'float g=fbm(p*9.)*.06+fbm(p*40.)*.03;vec2 r=mat2(.87,-.5,.5,.87)*p;',
      'float bars=smoothstep(.15,.55,.5+.5*sin(r.x*14.+T*.35+sin(r.y*1.5+T*.2)*.6));',
      'float leaf=smoothstep(.45,.75,fbm(p*2.2+vec2(T*.06,-T*.04)));',
      'float light=bars*(1.-leaf*.85)*smoothstep(1.3,.2,length(p-vec2(.3,-.1)));',
      'vec3 col=mix(shade,stone,.35+g);col=mix(col,warm,light*.75);return col;}'
    ].join('\n')
  };
  var COMMON = [
    'precision highp float;uniform vec2 R;uniform float T;',
    'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
    'float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);',
    'return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}',
    'float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return v;}'
  ].join('\n');

  window.SCENE = function (canvas, mode, opts) {
    opts = opts || {};
    var gl = canvas.getContext('webgl', { preserveDrawingBuffer: true, antialias: false });
    if (!gl) return null;
    var vs = 'attribute vec2 a;void main(){gl_Position=vec4(a,0,1);}';
    var fs = COMMON + '\n' + FRAG[mode] + '\nvoid main(){vec2 p=(gl_FragCoord.xy-.5*R)/R.y;vec3 c=scene(p,T);' +
      'c+= (h(gl_FragCoord.xy+T)-.5)*.025;gl_FragColor=vec4(c,1);}';
    function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
    var pr = gl.createProgram();
    gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(pr); gl.useProgram(pr);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, 'a'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var uR = gl.getUniformLocation(pr, 'R'), uT = gl.getUniformLocation(pr, 'T');
    var scale = opts.scale || 1;
    function fit() {
      var w = Math.round(canvas.clientWidth * scale), hh = Math.round(canvas.clientHeight * scale);
      if (canvas.width !== w || canvas.height !== hh) { canvas.width = w; canvas.height = hh; }
      gl.viewport(0, 0, canvas.width, canvas.height);
    }
    function render(t) { fit(); gl.uniform2f(uR, canvas.width, canvas.height); gl.uniform1f(uT, t); gl.drawArrays(gl.TRIANGLES, 0, 3); }
    window.renderAt = render;
    if (opts.still != null) render(opts.still);
    else { var t0 = performance.now(); (function loop(now) { render((now - t0) / 1000); requestAnimationFrame(loop); })(t0); }
    return render;
  };
})();
