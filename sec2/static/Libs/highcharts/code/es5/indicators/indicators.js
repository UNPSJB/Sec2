!/**
 * Highstock JS v11.4.1 (2024-04-04)
 *
 * Indicator series type for Highcharts Stock
 *
 * (c) 2010-2024 Pawel Fus, Sebastian Bochan
 *
 * License: www.highcharts.com/license
 */function(t){"object"==typeof module&&module.exports?(t.default=t,module.exports=t):"function"==typeof define&&define.amd?define("highcharts/indicators/indicators",["highcharts","highcharts/modules/stock"],function(e){return t(e),t.Highcharts=e,t}):t("undefined"!=typeof Highcharts?Highcharts:void 0)}(function(t){"use strict";var e=t?t._modules:{};function a(t,e,a,i){t.hasOwnProperty(e)||(t[e]=i.apply(null,a),"function"==typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:e,module:t[e]}})))}a(e,"Stock/Indicators/SMA/SMAIndicator.js",[e["Core/Chart/Chart.js"],e["Core/Series/SeriesRegistry.js"],e["Core/Utilities.js"]],function(t,e,a){var i,n=this&&this.__extends||(i=function(t,e){return(i=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a])})(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw TypeError("Class extends value "+String(e)+" is not a constructor or null");function a(){this.constructor=t}i(t,e),t.prototype=null===e?Object.create(e):(a.prototype=e.prototype,new a)}),o=e.seriesTypes.line,r=a.addEvent,s=a.fireEvent,p=a.error,l=a.extend,c=a.isArray,h=a.merge,u=a.pick,d=a.splat,f=function(e){function a(){return null!==e&&e.apply(this,arguments)||this}return n(a,e),a.prototype.destroy=function(){this.dataEventsToUnbind.forEach(function(t){t()}),e.prototype.destroy.apply(this,arguments)},a.prototype.getName=function(){var t=[],e=this.name;return e||((this.nameComponents||[]).forEach(function(e,a){t.push(this.options.params[e]+u(this.nameSuffixes[a],""))},this),e=(this.nameBase||this.type.toUpperCase())+(this.nameComponents?" ("+t.join(", ")+")":"")),e},a.prototype.getValues=function(t,e){var a,i,n=e.period,o=t.xData,r=t.yData,s=r.length,p=[],l=[],h=[],u=-1,d=0,f=0;if(!(o.length<n)){for(c(r[0])&&(u=e.index?e.index:0);d<n-1;)f+=u<0?r[d]:r[d][u],d++;for(a=d;a<s;a++)f+=u<0?r[a]:r[a][u],i=[o[a],f/n],p.push(i),l.push(i[0]),h.push(i[1]),f-=u<0?r[a-d]:r[a-d][u];return{values:p,xData:l,yData:h}}},a.prototype.init=function(a,i){var n=this;e.prototype.init.call(n,a,i);var o=r(t,"afterLinkSeries",function(t){if(!t.isUpdating){var e=!!n.dataEventsToUnbind.length;if(!n.linkedParent)return p("Series "+n.options.linkedTo+" not found! Check `linkedTo`.",!1,a);if(!e&&(n.dataEventsToUnbind.push(r(n.linkedParent,"updatedData",function(){n.recalculateValues()})),n.calculateOn.xAxis&&n.dataEventsToUnbind.push(r(n.linkedParent.xAxis,n.calculateOn.xAxis,function(){n.recalculateValues()}))),"init"===n.calculateOn.chart)n.processedYData||n.recalculateValues();else if(!e)var i=r(n.chart,n.calculateOn.chart,function(){n.recalculateValues(),i()})}},{order:0});n.dataEventsToUnbind=[],n.eventsToUnbind.push(o)},a.prototype.recalculateValues=function(){var t,e,a,i,n,o,r=[],p=this.points||[],l=(this.xData||[]).length,c=!0,h=this.linkedParent.options&&this.linkedParent.yData&&this.linkedParent.yData.length&&this.getValues(this.linkedParent,this.options.params)||{values:[],xData:[],yData:[]};if(l&&!this.hasGroupedData&&this.visible&&this.points){if(this.cropped){for(this.xAxis&&(i=this.xAxis.min,n=this.xAxis.max),a=this.cropData(h.xData,h.yData,i,n),o=0;o<a.xData.length;o++)r.push([a.xData[o]].concat(d(a.yData[o])));t=h.xData.indexOf(this.xData[0]),e=h.xData.indexOf(this.xData[this.xData.length-1]),-1===t&&e===h.xData.length-2&&r[0][0]===p[0].x&&r.shift(),this.updateData(r)}else(this.updateAllPoints||h.xData.length!==l-1&&h.xData.length!==l+1)&&(c=!1,this.updateData(h.values))}c&&(this.xData=h.xData,this.yData=h.yData,this.options.data=h.values),this.calculateOn.xAxis&&this.processedXData&&(delete this.processedXData,this.isDirty=!0,this.redraw()),this.isDirtyData=!!this.linkedSeries.length,s(this,"updatedData")},a.prototype.processData=function(){var t=this.options.compareToMain,a=this.linkedParent;e.prototype.processData.apply(this,arguments),this.dataModify&&a&&a.dataModify&&a.dataModify.compareValue&&t&&(this.dataModify.compareValue=a.dataModify.compareValue)},a.defaultOptions=h(o.defaultOptions,{name:void 0,tooltip:{valueDecimals:4},linkedTo:void 0,compareToMain:!1,params:{index:3,period:14}}),a}(o);return l(f.prototype,{calculateOn:{chart:"init"},hasDerivedData:!0,nameComponents:["period"],nameSuffixes:[],useCommonDataGrouping:!0}),e.registerSeriesType("sma",f),f}),a(e,"Stock/Indicators/EMA/EMAIndicator.js",[e["Core/Series/SeriesRegistry.js"],e["Core/Utilities.js"]],function(t,e){var a,i=this&&this.__extends||(a=function(t,e){return(a=Object.setPrototypeOf||({__proto__:[]})instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a])})(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw TypeError("Class extends value "+String(e)+" is not a constructor or null");function i(){this.constructor=t}a(t,e),t.prototype=null===e?Object.create(e):(i.prototype=e.prototype,new i)}),n=t.seriesTypes.sma,o=e.correctFloat,r=e.isArray,s=e.merge,p=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return i(e,t),e.prototype.accumulatePeriodPoints=function(t,e,a){for(var i=0,n=0;n<t;)i+=e<0?a[n]:a[n][e],n++;return i},e.prototype.calculateEma=function(t,e,a,i,n,r,s){var p=t[a-1],l=r<0?e[a-1]:e[a-1][r];return[p,void 0===n?s:o(l*i+n*(1-i))]},e.prototype.getValues=function(t,e){var a,i,n,o=e.period,s=t.xData,p=t.yData,l=p?p.length:0,c=2/(o+1),h=[],u=[],d=[],f=-1,y=0;if(!(l<o)){for(r(p[0])&&(f=e.index?e.index:0),y=this.accumulatePeriodPoints(o,f,p)/o,n=o;n<l+1;n++)i=this.calculateEma(s,p,n,c,a,f,y),h.push(i),u.push(i[0]),d.push(i[1]),a=i[1];return{values:h,xData:u,yData:d}}},e.defaultOptions=s(n.defaultOptions,{params:{index:3,period:9}}),e}(n);return t.registerSeriesType("ema",p),p}),a(e,"Stock/Indicators/MultipleLinesComposition.js",[e["Core/Series/SeriesRegistry.js"],e["Core/Utilities.js"]],function(t,e){var a,i=t.seriesTypes.sma.prototype,n=e.defined,o=e.error,r=e.merge;return function(t){var e=["bottomLine"],a=["top","bottom"],s=["top"];function p(t){return"plot"+t.charAt(0).toUpperCase()+t.slice(1)}function l(t,e){var a=[];return(t.pointArrayMap||[]).forEach(function(t){t!==e&&a.push(p(t))}),a}function c(){var t,e=this,a=e.pointValKey,s=e.linesApiNames,c=e.areaLinesNames,h=e.points,u=e.options,d=e.graph,f={options:{gapSize:u.gapSize}},y=[],m=l(e,a),x=h.length;if(m.forEach(function(e,a){for(y[a]=[];x--;)t=h[x],y[a].push({x:t.x,plotX:t.plotX,plotY:t[e],isNull:!n(t[e])});x=h.length}),e.userOptions.fillColor&&c.length){var g=y[m.indexOf(p(c[0]))],v=1===c.length?h:y[m.indexOf(p(c[1]))],D=e.color;e.points=v,e.nextPoints=g,e.color=e.userOptions.fillColor,e.options=r(h,f),e.graph=e.area,e.fillGraph=!0,i.drawGraph.call(e),e.area=e.graph,delete e.nextPoints,delete e.fillGraph,e.color=D}s.forEach(function(t,a){y[a]?(e.points=y[a],u[t]?e.options=r(u[t].styles,f):o('Error: "There is no '+t+' in DOCS options declared. Check if linesApiNames are consistent with your DOCS line names."'),e.graph=e["graph"+t],i.drawGraph.call(e),e["graph"+t]=e.graph):o('Error: "'+t+" doesn't have equivalent in pointArrayMap. To many elements in linesApiNames relative to pointArrayMap.\"")}),e.points=h,e.options=u,e.graph=d,i.drawGraph.call(e)}function h(t){var e,a=[],n=[];if(t=t||this.points,this.fillGraph&&this.nextPoints){if((e=i.getGraphPath.call(this,this.nextPoints))&&e.length){e[0][0]="L",a=i.getGraphPath.call(this,t),n=e.slice(0,a.length);for(var o=n.length-1;o>=0;o--)a.push(n[o])}}else a=i.getGraphPath.apply(this,arguments);return a}function u(t){var e=[];return(this.pointArrayMap||[]).forEach(function(a){e.push(t[a])}),e}function d(){var t,e=this,a=this.pointArrayMap,n=[];n=l(this),i.translate.apply(this,arguments),this.points.forEach(function(i){a.forEach(function(a,o){t=i[a],e.dataModify&&(t=e.dataModify.modifyValue(t)),null!==t&&(i[n[o]]=e.yAxis.toPixels(t,!0))})})}t.compose=function(t){var i=t.prototype;return i.linesApiNames=i.linesApiNames||e.slice(),i.pointArrayMap=i.pointArrayMap||a.slice(),i.pointValKey=i.pointValKey||"top",i.areaLinesNames=i.areaLinesNames||s.slice(),i.drawGraph=c,i.getGraphPath=h,i.toYData=u,i.translate=d,t}}(a||(a={})),a}),a(e,"masters/indicators/indicators.src.js",[e["Core/Globals.js"],e["Stock/Indicators/MultipleLinesComposition.js"]],function(t,e){return t.MultipleLinesComposition=t.MultipleLinesComposition||e,t})});