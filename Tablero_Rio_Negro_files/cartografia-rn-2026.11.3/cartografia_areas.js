/* Colocación de rótulos en pantalla. Las máscaras sólo se usan para rotular. */
(function(){
  'use strict';
  window.CartografiaAreales={crear:function(map,el,features,opciones){
    opciones=opciones||{};features=features||window.CartografiaMascaras;
    var nacional=!!opciones.nacional, canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
    var pane=map.getPane('rotulos-areales')||map.createPane('rotulos-areales');
    pane.style.zIndex=441;pane.style.pointerEvents='none';
    function orientarEstacion(l){
      if(!l.getLatLng||!l.options.icon||l.options.icon.options.className!=='estacion-ferroviaria')return;
      var ll=l.getLatLng(),dato=(window.CartografiaEstaciones||[]).find(function(v){return Math.abs(v.lat-ll.lat)<.00002&&Math.abs(v.lng-ll.lng)<.00002;});
      if(!dato)return;
      var svg='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><rect x="5" y="6" width="6" height="4" fill="#202020" transform="rotate('+dato.angulo+' 8 8)"/></svg>';
      l.setIcon(L.icon({iconUrl:'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg),iconSize:[16,16],iconAnchor:[8,8],className:'estacion-ferroviaria'}));
    }
    map.eachLayer(orientarEstacion);
    var estaciones=map.layerManager&&map.layerManager.getLayerGroup('Estaciones ferroviarias');
    if(estaciones)estaciones.eachLayer(orientarEstacion);
    var registros=(features.features||[]).filter(function(f){return !!f.properties.nacional===nacional;}).map(function(f){
      return {f:f,marker:L.marker(f.properties.centro,{pane:'rotulos-areales',interactive:false,keyboard:false,
        icon:L.divIcon({className:'rotulo-areal-adaptado',html:'',iconSize:[1,1],iconAnchor:[0,0]}),opacity:0}).addTo(map)};
    });
    el.classList.add(nacional?'rotulos-nacionales-ajustados':'rotulos-provinciales-ajustados');
    function dentroAnillo(x,y,r){var c=false;for(var i=0,j=r.length-1;i<r.length;j=i++){
      var a=r[i],b=r[j];if((a.y>y)!==(b.y>y)&&x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x)c=!c;
    }return c;}
    function dentro(x,y,polys){return polys.some(function(p){return dentroAnillo(x,y,p[0])&&!p.slice(1).some(function(h){return dentroAnillo(x,y,h);});});}
    function toca(a,b,g){g=g||4;return !(a.r+g<b.l||a.l-g>b.r||a.b+g<b.t||a.t-g>b.b);}
    function lineas(nombre){var w=nombre.split(/\s+/),a=[[nombre]];
      for(var i=1;i<w.length;i++)a.push([w.slice(0,i).join(' '),w.slice(i).join(' ')]);
      if(w.length>=4)for(var j=1;j<w.length-1;j++)for(var k=j+1;k<w.length;k++)a.push([w.slice(0,j).join(' '),w.slice(j,k).join(' '),w.slice(k).join(' ')]);
      return a;
    }
    function cajaDentro(r,polys){
      for(var x=r.l;x<=r.r+.1;x+=Math.max(1,(r.r-r.l)/8))if(!dentro(x,r.t,polys)||!dentro(x,r.b,polys))return false;
      for(var y=r.t;y<=r.b+.1;y+=Math.max(1,(r.b-r.t)/4))if(!dentro(r.l,y,polys)||!dentro(r.r,y,polys))return false;
      return dentro((r.l+r.r)/2,(r.t+r.b)/2,polys);
    }
    function actualizar(activos,nivel){
      if(!map._loaded||!el.clientWidth||!el.clientHeight)return;
      var z=map.getZoom(),sz=map.getSize(),base=el.getBoundingClientRect(),ocupados=[];
      el.querySelectorAll('.leaflet-control,.rotulo-pais,.rotulo-agua,.rotulo-sanitaria,.rotulo-gobierno,.rotulo-asentamiento,.mini-torta,.rotulo-central,.rotulo-vmos').forEach(function(n){
        var r=n.getBoundingClientRect();if(r.width&&r.height&&r.width<sz.x*.9&&r.height<sz.y*.9&&getComputedStyle(n).visibility!=='hidden')ocupados.push({l:r.left-base.left,r:r.right-base.left,t:r.top-base.top,b:r.bottom-base.top});
      });
      registros.forEach(function(o){o.marker.setOpacity(0);});
      registros.slice().sort(function(a,b){
        function prioridad(o){return o.f.properties.categoria==='departamento'?0:(o.f.properties.codigo==='62'?1:2);}
        return prioridad(a)-prioridad(b);
      }).forEach(function(o){
        var p=o.f.properties,dep=p.categoria==='departamento';
        if(dep&&(!(activos&&activos.has(p.grupo))||z<6.5))return;
        if(nacional&&p.codigo!=='62'&&z<(nivel||0)+1.4)return;
        var coords=o.f.geometry.type==='Polygon'?[o.f.geometry.coordinates]:o.f.geometry.coordinates;
        var polys=coords.map(function(poly){return poly.map(function(ring){return ring.map(function(c){return map.latLngToContainerPoint([c[1],c[0]]);});});});
        var puntos=[].concat.apply([],polys.map(function(poly){return poly[0];}));
        var l=Math.max(22,Math.min.apply(null,puntos.map(function(t){return t.x;}))),r=Math.min(sz.x-22,Math.max.apply(null,puntos.map(function(t){return t.x;})));
        var t=Math.max(22,Math.min.apply(null,puntos.map(function(t){return t.y;}))),b=Math.min(sz.y-22,Math.max.apply(null,puntos.map(function(t){return t.y;})));
        if(r-l<30||b-t<18)return;
        var centro=map.latLngToContainerPoint(p.centro),cx=Math.max(l,Math.min(r,centro.x)),cy=Math.max(t,Math.min(b,centro.y));
        var candidatos=[];
        for(var iy=0;iy<9;iy++)for(var ix=0;ix<9;ix++){
          var x=l+(r-l)*(ix+.5)/9,y=t+(b-t)*(iy+.5)/9;
          if(dentro(x,y,polys))candidatos.push({x:x,y:y,costo:Math.hypot((x-cx)/(r-l),(y-cy)/(b-t))});
        }
        if(dentro(cx,cy,polys))candidatos.push({x:cx,y:cy,costo:0});
        candidatos.sort(function(a,b){return a.costo-b.costo;});candidatos=candidatos.slice(0,nacional?70:30);
        o.diagnostico={caja:{l:l,r:r,t:t,b:b},centro:centro,candidatos:candidatos.length,ocupados:ocupados.length};
        var nombre=p.nombre.toLocaleUpperCase('es'),variantes=lineas(nombre),mejor=null;
        var maxFont=nacional?(p.codigo==='62'?11:10):(dep?Math.min(15,11+(z-6.5)*.7):Math.min(20,14+(z-6)*.8));
        var minFont=nacional?7:(dep?10:12),peso=dep?'500':'600';
        for(var fs=maxFont;fs>=minFont;fs-=1){
          ctx.font=peso+' '+fs+'px Arial';
          candidatos.forEach(function(c){variantes.forEach(function(ls){
            var anchos=ls.map(function(v){return ctx.measureText(v).width;}),natural=Math.max.apply(null,anchos);
            // Aumenta el interletrado sólo si la caja completa cabe en el polígono.
            var maxEsp=nacional?Math.min(4,Math.floor(fs*.7)/2):(dep?4:Math.min(18,Math.floor(fs*1.8)/2)),esp=0;
            var objetivo=Math.min((r-l)*(dep?.56:.72),natural+maxEsp*(Math.max.apply(null,ls.map(function(v){return v.length;}))-1));
            var alto=fs*(nacional?1.15:1.3)*ls.length,anch=natural;
            for(var paso=0;paso<=Math.ceil(maxEsp*2);paso++){
              var e=Math.max(0,maxEsp-paso*.5);
              var palabra=dep?Math.min(5,e*.6):Math.min(24,e*1.6);
              var aa=Math.max.apply(null,ls.map(function(v,i){return anchos[i]+e*v.length+palabra*(v.split(' ').length-1);}));
              if(aa>Math.max(natural,objetivo)+.1)continue;
              var rr={l:c.x-aa/2-2,r:c.x+aa/2+2,t:c.y-alto/2-1,b:c.y+alto/2+1};
              if(rr.l>=22&&rr.r<=sz.x-22&&rr.t>=22&&rr.b<=sz.y-22&&cajaDentro(rr,polys)&&!ocupados.some(function(v){return toca(rr,v,5);})){
                esp=e;anch=aa;var score=c.costo*25+ls.length*3+(maxFont-fs)*6-Math.min(dep?20:28,aa/(r-l)*(dep?20:32));
                if(!mejor||score<mejor.score)mejor={x:c.x,y:c.y,ls:ls,fs:fs,esp:esp,palabra:palabra,rect:rr,score:score};
                break;
              }
            }
          });});
          if(mejor&&mejor.fs>=maxFont-1)break;
        }
        if(!mejor&&dep&&nombre.indexOf(' ')<0&&(b-t)>(r-l)*1.6){
          for(var fv=Math.min(12,maxFont);fv>=minFont&&!mejor;fv--){
            ctx.font=peso+' '+fv+'px Arial';var av=ctx.measureText(nombre).width+4,hv=fv*1.3+4;
            candidatos.some(function(c){var rr={l:c.x-hv/2,r:c.x+hv/2,t:c.y-av/2,b:c.y+av/2};
              if(rr.l>=22&&rr.r<=sz.x-22&&rr.t>=22&&rr.b<=sz.y-22&&cajaDentro(rr,polys)&&!ocupados.some(function(v){return toca(rr,v,5);})){
                mejor={x:c.x,y:c.y,ls:[nombre],fs:fv,esp:0,rect:rr,vertical:true};return true;
              }return false;
            });
          }
        }
        if(!mejor)return;
        var node=o.marker.getElement(),span=document.createElement('span');
        span.className='texto-areal '+(dep?'areal-departamento':'areal-provincia');
        span.style.left='0';span.style.top='0';
        if(nacional&&p.codigo==='62')span.classList.add('areal-rn-nacional');
        span.style.fontSize=mejor.fs+'px';span.style.fontWeight=peso;span.style.letterSpacing=mejor.esp+'px';
        span.style.wordSpacing=(mejor.palabra||0)+'px';span.style.lineHeight=nacional?'1.15':'1.3';
        if(mejor.vertical)span.style.transform='translate(-50%,-50%) rotate(-90deg)';
        // Tanto el interletrado como el espacio entre palabras entran en la caja.
        mejor.ls.forEach(function(v,i){if(i)span.appendChild(document.createElement('br'));span.appendChild(document.createTextNode(v));});
        node.replaceChildren(span);node.dataset.nombre=p.nombre;node.dataset.categoria=p.categoria;
        node.dataset.caja=JSON.stringify(mejor.rect);node.dataset.codigo=p.codigo;
        o.marker.setLatLng(map.containerPointToLatLng([mejor.x,mejor.y]));o.marker.setOpacity(1);ocupados.push(mejor.rect);
      });
    }
    var api={actualizar:actualizar,registros:registros};el._cartografiaAreal=api;return api;
  }};
})();
