!/**
 * Highcharts JS v11.4.1 (2024-04-04)
 *
 * Exporting module
 *
 * (c) 2010-2024 Torstein Honsi
 *
 * License: www.highcharts.com/license
 */function(e){"object"==typeof module&&module.exports?(e.default=e,module.exports=e):"function"==typeof define&&define.amd?define("highcharts/modules/exporting",["highcharts"],function(t){return e(t),e.Highcharts=t,e}):e("undefined"!=typeof Highcharts?Highcharts:void 0)}(function(e){"use strict";var t=e?e._modules:{};function n(e,t,n,i){e.hasOwnProperty(t)||(e[t]=i.apply(null,n),"function"==typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:t,module:e[t]}})))}n(t,"Core/Chart/ChartNavigationComposition.js",[],function(){var e,t,n;return(t=e||(e={})).compose=function(e){return e.navigation||(e.navigation=new n(e)),e},n=function(){function e(e){this.updates=[],this.chart=e}return e.prototype.addUpdate=function(e){this.chart.navigation.updates.push(e)},e.prototype.update=function(e,t){var n=this;this.updates.forEach(function(i){i.call(n.chart,e,t)})},e}(),t.Additions=n,e}),n(t,"Extensions/Exporting/ExportingDefaults.js",[t["Core/Globals.js"]],function(e){return{exporting:{allowTableSorting:!0,type:"image/png",url:"https://export.highcharts.com/",pdfFont:{normal:void 0,bold:void 0,bolditalic:void 0,italic:void 0},printMaxWidth:780,scale:2,buttons:{contextButton:{className:"highcharts-contextbutton",menuClassName:"highcharts-contextmenu",symbol:"menu",titleKey:"contextButtonTitle",menuItems:["viewFullscreen","printChart","separator","downloadPNG","downloadJPEG","downloadPDF","downloadSVG"]}},menuItemDefinitions:{viewFullscreen:{textKey:"viewFullscreen",onclick:function(){this.fullscreen&&this.fullscreen.toggle()}},printChart:{textKey:"printChart",onclick:function(){this.print()}},separator:{separator:!0},downloadPNG:{textKey:"downloadPNG",onclick:function(){this.exportChart()}},downloadJPEG:{textKey:"downloadJPEG",onclick:function(){this.exportChart({type:"image/jpeg"})}},downloadPDF:{textKey:"downloadPDF",onclick:function(){this.exportChart({type:"application/pdf"})}},downloadSVG:{textKey:"downloadSVG",onclick:function(){this.exportChart({type:"image/svg+xml"})}}}},lang:{viewFullscreen:"View in full screen",exitFullscreen:"Exit from full screen",printChart:"Print chart",downloadPNG:"Download PNG image",downloadJPEG:"Download JPEG image",downloadPDF:"Download PDF document",downloadSVG:"Download SVG vector image",contextButtonTitle:"Chart context menu"},navigation:{buttonOptions:{symbolSize:14,symbolX:14.5,symbolY:13.5,align:"right",buttonSpacing:3,height:28,verticalAlign:"top",width:28,symbolFill:"#666666",symbolStroke:"#666666",symbolStrokeWidth:3,theme:{padding:5}},menuStyle:{border:"none",borderRadius:"3px",background:"#ffffff",padding:"0.5em"},menuItemStyle:{background:"none",borderRadius:"3px",color:"#333333",padding:"0.5em",fontSize:e.isTouchDevice?"0.9em":"0.8em",transition:"background 250ms, color 250ms"},menuItemHoverStyle:{background:"#f2f2f2"}}}}),n(t,"Extensions/Exporting/ExportingSymbols.js",[],function(){var e;return function(e){var t=[];function n(e,t,n,i){return[["M",e,t+2.5],["L",e+n,t+2.5],["M",e,t+i/2+.5],["L",e+n,t+i/2+.5],["M",e,t+i-1.5],["L",e+n,t+i-1.5]]}function i(e,t,n,i){var o=i/3-2;return[].concat(this.circle(n-o,t,o,o),this.circle(n-o,t+o+4,o,o),this.circle(n-o,t+2*(o+4),o,o))}e.compose=function(e){if(-1===t.indexOf(e)){t.push(e);var o=e.prototype.symbols;o.menu=n,o.menuball=i.bind(o)}}}(e||(e={})),e}),n(t,"Extensions/Exporting/Fullscreen.js",[t["Core/Renderer/HTML/AST.js"],t["Core/Globals.js"],t["Core/Utilities.js"]],function(e,t,n){var i=t.composed,o=n.addEvent,r=n.fireEvent,s=n.pushUnique;function a(){this.fullscreen=new l(this)}var l=function(){function t(e){this.chart=e,this.isOpen=!1;var t=e.renderTo;!this.browserProps&&("function"==typeof t.requestFullscreen?this.browserProps={fullscreenChange:"fullscreenchange",requestFullscreen:"requestFullscreen",exitFullscreen:"exitFullscreen"}:t.mozRequestFullScreen?this.browserProps={fullscreenChange:"mozfullscreenchange",requestFullscreen:"mozRequestFullScreen",exitFullscreen:"mozCancelFullScreen"}:t.webkitRequestFullScreen?this.browserProps={fullscreenChange:"webkitfullscreenchange",requestFullscreen:"webkitRequestFullScreen",exitFullscreen:"webkitExitFullscreen"}:t.msRequestFullscreen&&(this.browserProps={fullscreenChange:"MSFullscreenChange",requestFullscreen:"msRequestFullscreen",exitFullscreen:"msExitFullscreen"}))}return t.compose=function(e){s(i,"Fullscreen")&&o(e,"beforeRender",a)},t.prototype.close=function(){var e=this,t=e.chart,n=t.options.chart;r(t,"fullscreenClose",null,function(){e.isOpen&&e.browserProps&&t.container.ownerDocument instanceof Document&&t.container.ownerDocument[e.browserProps.exitFullscreen](),e.unbindFullscreenEvent&&(e.unbindFullscreenEvent=e.unbindFullscreenEvent()),t.setSize(e.origWidth,e.origHeight,!1),e.origWidth=void 0,e.origHeight=void 0,n.width=e.origWidthOption,n.height=e.origHeightOption,e.origWidthOption=void 0,e.origHeightOption=void 0,e.isOpen=!1,e.setButtonText()})},t.prototype.open=function(){var e=this,t=e.chart,n=t.options.chart;r(t,"fullscreenOpen",null,function(){if(n&&(e.origWidthOption=n.width,e.origHeightOption=n.height),e.origWidth=t.chartWidth,e.origHeight=t.chartHeight,e.browserProps){var i=o(t.container.ownerDocument,e.browserProps.fullscreenChange,function(){e.isOpen?(e.isOpen=!1,e.close()):(t.setSize(null,null,!1),e.isOpen=!0,e.setButtonText())}),r=o(t,"destroy",i);e.unbindFullscreenEvent=function(){i(),r()};var s=t.renderTo[e.browserProps.requestFullscreen]();s&&s.catch(function(){alert("Full screen is not supported inside a frame.")})}})},t.prototype.setButtonText=function(){var t=this.chart,n=t.exportDivElements,i=t.options.exporting,o=i&&i.buttons&&i.buttons.contextButton.menuItems,r=t.options.lang;if(i&&i.menuItemDefinitions&&r&&r.exitFullscreen&&r.viewFullscreen&&o&&n){var s=n[o.indexOf("viewFullscreen")];s&&e.setElementHTML(s,this.isOpen?r.exitFullscreen:i.menuItemDefinitions.viewFullscreen.text||r.viewFullscreen)}},t.prototype.toggle=function(){this.isOpen?this.close():this.open()},t}();return l}),n(t,"Core/HttpUtilities.js",[t["Core/Globals.js"],t["Core/Utilities.js"]],function(e,t){var n=this&&this.__assign||function(){return(n=Object.assign||function(e){for(var t,n=1,i=arguments.length;n<i;n++)for(var o in t=arguments[n])Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o]);return e}).apply(this,arguments)},i=e.win,o=t.discardElement,r=t.objectEach,s={ajax:function(e){var t={json:"application/json",xml:"application/xml",text:"text/plain",octet:"application/octet-stream"},n=new XMLHttpRequest;function i(t,n){e.error&&e.error(t,n)}if(!e.url)return!1;n.open((e.type||"get").toUpperCase(),e.url,!0),e.headers&&e.headers["Content-Type"]||n.setRequestHeader("Content-Type",t[e.dataType||"json"]||t.text),r(e.headers,function(e,t){n.setRequestHeader(t,e)}),e.responseType&&(n.responseType=e.responseType),n.onreadystatechange=function(){var t;if(4===n.readyState){if(200===n.status){if("blob"!==e.responseType&&(t=n.responseText,"json"===e.dataType))try{t=JSON.parse(t)}catch(e){if(e instanceof Error)return i(n,e)}return e.success&&e.success(t,n)}i(n,n.responseText)}},e.data&&"string"!=typeof e.data&&(e.data=JSON.stringify(e.data)),n.send(e.data)},getJSON:function(e,t){s.ajax({url:e,success:t,dataType:"json",headers:{"Content-Type":"text/plain"}})},post:function(e,t,s){var a=new i.FormData;r(t,function(e,t){a.append(t,e)}),a.append("b64","true");var l=t.filename,c=t.type;return i.fetch(e,n({method:"POST",body:a},s)).then(function(e){e.ok&&e.text().then(function(e){var t=document.createElement("a");t.href="data:".concat(c,";base64,").concat(e),t.download=l,t.click(),o(t)})})}};return s}),n(t,"Extensions/Exporting/Exporting.js",[t["Core/Renderer/HTML/AST.js"],t["Core/Chart/Chart.js"],t["Core/Chart/ChartNavigationComposition.js"],t["Core/Defaults.js"],t["Extensions/Exporting/ExportingDefaults.js"],t["Extensions/Exporting/ExportingSymbols.js"],t["Extensions/Exporting/Fullscreen.js"],t["Core/Globals.js"],t["Core/HttpUtilities.js"],t["Core/Utilities.js"]],function(e,t,n,i,o,r,s,a,l,c){var u,p=this&&this.__assign||function(){return(p=Object.assign||function(e){for(var t,n=1,i=arguments.length;n<i;n++)for(var o in t=arguments[n])Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o]);return e}).apply(this,arguments)},h=i.defaultOptions,d=a.doc,f=a.SVG_NS,g=a.win,m=c.addEvent,x=c.css,v=c.createElement,y=c.discardElement,b=c.extend,w=c.find,E=c.fireEvent,C=c.isObject,S=c.merge,O=c.objectEach,T=c.pick,F=c.removeEvent,P=c.uniqueKey;return function(t){var i,u=[/-/,/^(clipPath|cssText|d|height|width)$/,/^font$/,/[lL]ogical(Width|Height)$/,/^parentRule$/,/^(cssRules|ownerRules)$/,/perspective/,/TapHighlightColor/,/^transition/,/^length$/,/^[0-9]+$/],k=["fill","stroke","strokeLinecap","strokeLinejoin","strokeWidth","textAnchor","x","y"];t.inlineAllowlist=[];var j=["clipPath","defs","desc"];function M(e){var t,n,i=this,o=i.renderer,r=S(i.options.navigation.buttonOptions,e),s=r.onclick,a=r.menuItems,l=r.symbolSize||12;if(i.btnCount||(i.btnCount=0),i.exportDivElements||(i.exportDivElements=[],i.exportSVGElements=[]),!1!==r.enabled&&r.theme){var c=r.theme;i.styledMode||(c.fill=T(c.fill,"#ffffff"),c.stroke=T(c.stroke,"none")),s?n=function(e){e&&e.stopPropagation(),s.call(i,e)}:a&&(n=function(e){e&&e.stopPropagation(),i.contextMenu(u.menuClassName,a,u.translateX||0,u.translateY||0,u.width||0,u.height||0,u),u.setState(2)}),r.text&&r.symbol?c.paddingLeft=T(c.paddingLeft,30):r.text||b(c,{width:r.width,height:r.height,padding:0}),i.styledMode||(c["stroke-linecap"]="round",c.fill=T(c.fill,"#ffffff"),c.stroke=T(c.stroke,"none"));var u=o.button(r.text,0,0,n,c,void 0,void 0,void 0,void 0,r.useHTML).addClass(e.className).attr({title:T(i.options.lang[r._titleKey||r.titleKey],"")});u.menuClassName=e.menuClassName||"highcharts-menu-"+i.btnCount++,r.symbol&&(t=o.symbol(r.symbol,r.symbolX-l/2,r.symbolY-l/2,l,l,{width:l,height:l}).addClass("highcharts-button-symbol").attr({zIndex:1}).add(u),i.styledMode||t.attr({stroke:r.symbolStroke,fill:r.symbolFill,"stroke-width":r.symbolStrokeWidth||1})),u.add(i.exportingGroup).align(b(r,{width:u.width,x:T(r.x,i.buttonOffset)}),!0,"spacingBox"),i.buttonOffset+=((u.width||0)+r.buttonSpacing)*("right"===r.align?-1:1),i.exportSVGElements.push(u,t)}}function N(){if(this.printReverseInfo){var e=this.printReverseInfo,t=e.childNodes,n=e.origDisplay,o=e.resetParams;this.moveContainers(this.renderTo),[].forEach.call(t,function(e,t){1===e.nodeType&&(e.style.display=n[t]||"")}),this.isPrinting=!1,o&&this.setSize.apply(this,o),delete this.printReverseInfo,i=void 0,E(this,"afterPrint")}}function H(){var e,t=d.body,n=this.options.exporting.printMaxWidth,i={childNodes:t.childNodes,origDisplay:[],resetParams:void 0};this.isPrinting=!0,null===(e=this.pointer)||void 0===e||e.reset(void 0,0),E(this,"beforePrint"),n&&this.chartWidth>n&&(i.resetParams=[this.options.chart.width,void 0,!1],this.setSize(n,void 0,!1)),[].forEach.call(i.childNodes,function(e,t){1===e.nodeType&&(i.origDisplay[t]=e.style.display,e.style.display="none")}),this.moveContainers(t),this.printReverseInfo=i}function D(e){e.renderExporting(),m(e,"redraw",e.renderExporting),m(e,"destroy",e.destroyExport)}function G(t,n,i,o,r,s,a){var l,u,h=this,f=h.options.navigation,y=h.chartWidth,w=h.chartHeight,S="cache-"+t,O=Math.max(r,s),T=h[S];T||(h.exportContextMenu=h[S]=T=v("div",{className:t},p({position:"absolute",zIndex:1e3,padding:O+"px",pointerEvents:"auto"},h.renderer.style),(null===(l=h.scrollablePlotArea)||void 0===l?void 0:l.fixedDiv)||h.container),u=v("ul",{className:"highcharts-menu"},h.styledMode?{}:{listStyle:"none",margin:0,padding:0},T),h.styledMode||x(u,b({MozBoxShadow:"3px 3px 10px #888",WebkitBoxShadow:"3px 3px 10px #888",boxShadow:"3px 3px 10px #888"},f.menuStyle)),T.hideMenu=function(){x(T,{display:"none"}),a&&a.setState(0),h.openMenu=!1,x(h.renderTo,{overflow:"hidden"}),x(h.container,{overflow:"hidden"}),c.clearTimeout(T.hideTimer),E(h,"exportMenuHidden")},h.exportEvents.push(m(T,"mouseleave",function(){T.hideTimer=g.setTimeout(T.hideMenu,500)}),m(T,"mouseenter",function(){c.clearTimeout(T.hideTimer)}),m(d,"mouseup",function(e){var n;(null===(n=h.pointer)||void 0===n?void 0:n.inClass(e.target,t))||T.hideMenu()}),m(T,"click",function(){h.openMenu&&T.hideMenu()})),n.forEach(function(t){if("string"==typeof t&&(t=h.options.exporting.menuItemDefinitions[t]),C(t,!0)){var n=void 0;t.separator?n=v("hr",void 0,void 0,u):("viewData"===t.textKey&&h.isDataTableVisible&&(t.textKey="hideData"),n=v("li",{className:"highcharts-menu-item",onclick:function(e){e&&e.stopPropagation(),T.hideMenu(),"string"!=typeof t&&t.onclick&&t.onclick.apply(h,arguments)}},void 0,u),e.setElementHTML(n,t.text||h.options.lang[t.textKey]),h.styledMode||(n.onmouseover=function(){x(this,f.menuItemHoverStyle)},n.onmouseout=function(){x(this,f.menuItemStyle)},x(n,b({cursor:"pointer"},f.menuItemStyle||{})))),h.exportDivElements.push(n)}}),h.exportDivElements.push(u,T),h.exportMenuWidth=T.offsetWidth,h.exportMenuHeight=T.offsetHeight);var F={display:"block"};i+h.exportMenuWidth>y?F.right=y-i-r-O+"px":F.left=i-O+"px",o+s+h.exportMenuHeight>w&&"top"!==a.alignOptions.verticalAlign?F.bottom=w-o-O+"px":F.top=o+s-O+"px",x(T,F),x(h.renderTo,{overflow:""}),x(h.container,{overflow:""}),h.openMenu=!0,E(h,"exportMenuShown")}function W(e){var t,n=e?e.target:this,i=n.exportSVGElements,o=n.exportDivElements,r=n.exportEvents;i&&(i.forEach(function(e,o){e&&(e.onclick=e.ontouchstart=null,n[t="cache-"+e.menuClassName]&&delete n[t],i[o]=e.destroy())}),i.length=0),n.exportingGroup&&(n.exportingGroup.destroy(),delete n.exportingGroup),o&&(o.forEach(function(e,t){e&&(c.clearTimeout(e.hideTimer),F(e,"mouseleave"),o[t]=e.onmouseout=e.onmouseover=e.ontouchstart=e.onclick=null,y(e))}),o.length=0),r&&(r.forEach(function(e){e()}),r.length=0)}function I(e,t){var n=this.getSVGForExport(e,t);e=S(this.options.exporting,e),l.post(e.url,{filename:e.filename?e.filename.replace(/\//g,"-"):this.getFilename(),type:e.type,width:e.width,scale:e.scale,svg:n},e.fetchOptions)}function R(){return this.styledMode&&this.inlineStyles(),this.container.innerHTML}function L(){var e=this.userOptions.title&&this.userOptions.title.text,t=this.options.exporting.filename;return t?t.replace(/\//g,"-"):("string"==typeof e&&(t=e.toLowerCase().replace(/<\/?[^>]+(>|$)/g,"").replace(/[\s_]+/g,"-").replace(/[^a-z0-9\-]/g,"").replace(/^[\-]+/g,"").replace(/[\-]+/g,"-").substr(0,24).replace(/[\-]+$/g,"")),(!t||t.length<5)&&(t="chart"),t)}function q(e){var t,n,i=S(this.options,e);i.plotOptions=S(this.userOptions.plotOptions,e&&e.plotOptions),i.time=S(this.userOptions.time,e&&e.time);var o=v("div",null,{position:"absolute",top:"-9999em",width:this.chartWidth+"px",height:this.chartHeight+"px"},d.body),r=this.renderTo.style.width,s=this.renderTo.style.height,a=i.exporting.sourceWidth||i.chart.width||/px$/.test(r)&&parseInt(r,10)||(i.isGantt?800:600),l=i.exporting.sourceHeight||i.chart.height||/px$/.test(s)&&parseInt(s,10)||400;b(i.chart,{animation:!1,renderTo:o,forExport:!0,renderer:"SVGRenderer",width:a,height:l}),i.exporting.enabled=!1,delete i.data,i.series=[],this.series.forEach(function(e){(n=S(e.userOptions,{animation:!1,enableMouseTracking:!1,showCheckbox:!1,visible:e.visible})).isInternal||i.series.push(n)});var c={};this.axes.forEach(function(e){e.userOptions.internalKey||(e.userOptions.internalKey=P()),e.options.isInternal||(c[e.coll]||(c[e.coll]=!0,i[e.coll]=[]),i[e.coll].push(S(e.userOptions,{visible:e.visible})))}),i.colorAxis=this.userOptions.colorAxis;var u=new this.constructor(i,this.callback);return e&&["xAxis","yAxis","series"].forEach(function(t){var n={};e[t]&&(n[t]=e[t],u.update(n))}),this.axes.forEach(function(e){var t=w(u.axes,function(t){return t.options.internalKey===e.userOptions.internalKey}),n=e.getExtremes(),i=n.userMin,o=n.userMax;t&&(void 0!==i&&i!==t.min||void 0!==o&&o!==t.max)&&t.setExtremes(i,o,!0,!1)}),t=u.getChartHTML(),E(this,"getSVG",{chartCopy:u}),t=this.sanitizeSVG(t,i),i=null,u.destroy(),y(o),t}function V(e,t){var n=this.options.exporting;return this.getSVG(S({chart:{borderRadius:0}},n.chartOptions,t,{exporting:{sourceWidth:e&&e.sourceWidth||n.sourceWidth,sourceHeight:e&&e.sourceHeight||n.sourceHeight}}))}function z(){var e,n=t.inlineAllowlist,i={},o=d.createElement("iframe");x(o,{width:"1px",height:"1px",visibility:"hidden"}),d.body.appendChild(o);var r=o.contentWindow&&o.contentWindow.document;r&&r.body.appendChild(r.createElementNS(f,"svg")),function t(o){var s,l,c,p,h,d,f={};if(r&&1===o.nodeType&&-1===j.indexOf(o.nodeName)){if(s=g.getComputedStyle(o,null),l="svg"===o.nodeName?{}:g.getComputedStyle(o.parentNode,null),!i[o.nodeName]){e=r.getElementsByTagName("svg")[0],c=r.createElementNS(o.namespaceURI,o.nodeName),e.appendChild(c);var m=g.getComputedStyle(c,null),v={};for(var y in m)"string"!=typeof m[y]||/^[0-9]+$/.test(y)||(v[y]=m[y]);i[o.nodeName]=v,"text"===o.nodeName&&delete i.text.fill,e.removeChild(c)}for(var b in s)(a.isFirefox||a.isMS||a.isSafari||Object.hasOwnProperty.call(s,b))&&function(e,t){if(p=h=!1,n.length){for(d=n.length;d--&&!h;)h=n[d].test(t);p=!h}for("transform"===t&&"none"===e&&(p=!0),d=u.length;d--&&!p;)p=u[d].test(t)||"function"==typeof e;!p&&(l[t]!==e||"svg"===o.nodeName)&&i[o.nodeName][t]!==e&&(k&&-1===k.indexOf(t)?f[t]=e:e&&o.setAttribute(t.replace(/([A-Z])/g,function(e,t){return"-"+t.toLowerCase()}),e))}(s[b],b);if(x(o,f),"svg"===o.nodeName&&o.setAttribute("stroke-width","1px"),"text"===o.nodeName)return;[].forEach.call(o.children||o.childNodes,t)}}(this.container.querySelector("svg")),e.parentNode.removeChild(e),o.parentNode.removeChild(o)}function $(e){var t=this.scrollablePlotArea;(t?[t.fixedDiv,t.scrollingContainer]:[this.container]).forEach(function(t){e.appendChild(t)})}function A(){var e=this,t=function(t,n,i){e.isDirtyExporting=!0,S(!0,e.options[t],n),T(i,!0)&&e.redraw()};e.exporting={update:function(e,n){t("exporting",e,n)}},n.compose(e).navigation.addUpdate(function(e,n){t("navigation",e,n)})}function K(){var e=this;e.isPrinting||(i=e,a.isSafari||e.beforePrint(),setTimeout(function(){g.focus(),g.print(),a.isSafari||setTimeout(function(){e.afterPrint()},1e3)},1))}function U(){var e=this,t=e.options.exporting,n=t.buttons,i=e.isDirtyExporting||!e.exportSVGElements;e.buttonOffset=0,e.isDirtyExporting&&e.destroyExport(),i&&!1!==t.enabled&&(e.exportEvents=[],e.exportingGroup=e.exportingGroup||e.renderer.g("exporting-group").attr({zIndex:3}).add(),O(n,function(t){e.addButton(t)}),e.isDirtyExporting=!1)}function B(e,t){var n=e.indexOf("</svg>")+6,i=e.substr(n);return e=e.substr(0,n),t&&t.exporting&&t.exporting.allowHTML&&i&&(i='<foreignObject x="0" y="0" width="'+t.chart.width+'" height="'+t.chart.height+'"><body xmlns="http://www.w3.org/1999/xhtml">'+i.replace(/(<(?:img|br).*?(?=\>))>/g,"$1 />")+"</body></foreignObject>",e=e.replace("</svg>",i+"</svg>")),e=e.replace(/zIndex="[^"]+"/g,"").replace(/symbolName="[^"]+"/g,"").replace(/jQuery[0-9]+="[^"]+"/g,"").replace(/url\(("|&quot;)(.*?)("|&quot;)\;?\)/g,"url($2)").replace(/url\([^#]+#/g,"url(#").replace(/<svg /,'<svg xmlns:xlink="http://www.w3.org/1999/xlink" ').replace(/ (|NS[0-9]+\:)href=/g," xlink:href=").replace(/\n+/g," ").replace(/(fill|stroke)="rgba\(([ 0-9]+,[ 0-9]+,[ 0-9]+),([ 0-9\.]+)\)"/g,'$1="rgb($2)" $1-opacity="$3"').replace(/&nbsp;/g,"\xa0").replace(/&shy;/g,"\xad")}t.compose=function(e,t){r.compose(t),s.compose(e);var n=e.prototype;n.exportChart||(n.afterPrint=N,n.exportChart=I,n.inlineStyles=z,n.print=K,n.sanitizeSVG=B,n.getChartHTML=R,n.getSVG=q,n.getSVGForExport=V,n.getFilename=L,n.moveContainers=$,n.beforePrint=H,n.contextMenu=G,n.addButton=M,n.destroyExport=W,n.renderExporting=U,n.callbacks.push(D),m(e,"init",A),a.isSafari&&g.matchMedia("print").addListener(function(e){i&&(e.matches?i.beforePrint():i.afterPrint())}),h.exporting=S(o.exporting,h.exporting),h.lang=S(o.lang,h.lang),h.navigation=S(o.navigation,h.navigation))}}(u||(u={})),u}),n(t,"masters/modules/exporting.src.js",[t["Core/Globals.js"],t["Extensions/Exporting/Exporting.js"],t["Core/HttpUtilities.js"]],function(e,t,n){return e.HttpUtilities=e.HttpUtilities||n,e.ajax=e.HttpUtilities.ajax,e.getJSON=e.HttpUtilities.getJSON,e.post=e.HttpUtilities.post,t.compose(e.Chart,e.Renderer),e})});