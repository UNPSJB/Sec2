!/**
 * Highstock JS v11.4.1 (2024-04-04)
 *
 * Hollow Candlestick series type for Highcharts Stock
 *
 * (c) 2010-2024 Karol Kolodziej
 *
 * License: www.highcharts.com/license
 */function(t){"object"==typeof module&&module.exports?(t.default=t,module.exports=t):"function"==typeof define&&define.amd?define("highcharts/modules/hollowcandlestick",["highcharts","highcharts/modules/stock"],function(e){return t(e),t.Highcharts=e,t}):t("undefined"!=typeof Highcharts?Highcharts:void 0)}(function(t){"use strict";var e=t?t._modules:{};function i(t,e,i,s){t.hasOwnProperty(e)||(t[e]=s.apply(null,i),"function"==typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:e,module:t[e]}})))}i(e,"Series/HollowCandlestick/HollowCandlestickPoint.js",[e["Core/Series/SeriesRegistry.js"]],function(t){let{seriesTypes:{candlestick:e}}=t;class i extends e.prototype.pointClass{getClassName(){let t=super.getClassName.apply(this),e=this.index,i=this.series.hollowCandlestickData[e];return i.isBullish||"up"!==i.trendDirection||(t+="-bearish-up"),t}}return i}),i(e,"Series/HollowCandlestick/HollowCandlestickSeries.js",[e["Series/HollowCandlestick/HollowCandlestickPoint.js"],e["Core/Series/SeriesRegistry.js"],e["Core/Utilities.js"],e["Core/Axis/Axis.js"]],function(t,e,i,s){let{seriesTypes:{candlestick:o}}=e,{addEvent:l,merge:n}=i;class r extends o{constructor(){super(...arguments),this.hollowCandlestickData=[]}getPriceMovement(){let t=this.allGroupedData||this.yData,e=this.hollowCandlestickData;e.length=0,e.push({isBullish:!0,trendDirection:"up"});for(let i=1;i<t.length;i++){let s=t[i],o=t[i-1];e.push(this.isBullish(s,o))}}getLineColor(t){return"up"===t?this.options.upColor||"#06b535":this.options.color||"#f21313"}getPointFill(t){return t.isBullish?"transparent":"up"===t.trendDirection?this.options.upColor||"#06b535":this.options.color||"#f21313"}init(){super.init.apply(this,arguments),this.hollowCandlestickData=[]}isBullish(t,e){return{isBullish:t[0]<=t[3],trendDirection:t[3]<e[3]?"down":"up"}}pointAttribs(t,e){let i;let s=super.pointAttribs.call(this,t,e),o=t.index,l=this.hollowCandlestickData[o];return s.fill=this.getPointFill(l)||s.fill,s.stroke=this.getLineColor(l.trendDirection)||s.stroke,e&&(i=this.options.states[e],s.fill=i.color||s.fill,s.stroke=i.lineColor||s.stroke,s["stroke-width"]=i.lineWidth||s["stroke-width"]),s}}return r.defaultOptions=n(o.defaultOptions,{color:"#f21313",dataGrouping:{groupAll:!0,groupPixelWidth:10},lineColor:"#f21313",upColor:"#06b535",upLineColor:"#06b535"}),l(r,"updatedData",function(){this.hollowCandlestickData.length&&(this.hollowCandlestickData.length=0)}),l(s,"postProcessData",function(){this.series.forEach(function(t){t.is("hollowcandlestick")&&t.getPriceMovement()})}),r.prototype.pointClass=t,e.registerSeriesType("hollowcandlestick",r),r}),i(e,"masters/modules/hollowcandlestick.src.js",[e["Core/Globals.js"]],function(t){return t})});