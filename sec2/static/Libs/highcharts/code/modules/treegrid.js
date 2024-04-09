!/**
 * Highcharts Gantt JS v11.4.1 (2024-04-04)
 *
 * Tree Grid
 *
 * (c) 2016-2024 Jon Arild Nygard
 *
 * License: www.highcharts.com/license
 */function(e){"object"==typeof module&&module.exports?(e.default=e,module.exports=e):"function"==typeof define&&define.amd?define("highcharts/modules/treegrid",["highcharts"],function(t){return e(t),e.Highcharts=t,e}):e("undefined"!=typeof Highcharts?Highcharts:void 0)}(function(e){"use strict";var t=e?e._modules:{};function i(e,t,i,s){e.hasOwnProperty(t)||(e[t]=s.apply(null,i),"function"==typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:t,module:e[t]}})))}i(t,"Core/Axis/BrokenAxis.js",[t["Core/Axis/Stacking/StackItem.js"],t["Core/Utilities.js"]],function(e,t){var i;let{addEvent:s,find:o,fireEvent:r,isArray:n,isNumber:l,pick:a}=t;return function(t){function i(){void 0!==this.brokenAxis&&this.brokenAxis.setBreaks(this.options.breaks,!1)}function d(){this.brokenAxis?.hasBreaks&&(this.options.ordinal=!1)}function h(){let e=this.brokenAxis;if(e?.hasBreaks){let t=this.tickPositions,i=this.tickPositions.info,s=[];for(let i=0;i<t.length;i++)e.isInAnyBreak(t[i])||s.push(t[i]);this.tickPositions=s,this.tickPositions.info=i}}function c(){this.brokenAxis||(this.brokenAxis=new k(this))}function p(){let{isDirty:e,options:{connectNulls:t},points:i,xAxis:s,yAxis:o}=this;if(e){let e=i.length;for(;e--;){let r=i[e],n=!(null===r.y&&!1===t)&&(s?.brokenAxis?.isInAnyBreak(r.x,!0)||o?.brokenAxis?.isInAnyBreak(r.y,!0));r.visible=!n&&!1!==r.options.visible}}}function f(){this.drawBreaks(this.xAxis,["x"]),this.drawBreaks(this.yAxis,a(this.pointArrayMap,["y"]))}function u(e,t){let i,s,o;let n=this,d=n.points;if(e?.brokenAxis?.hasBreaks){let h=e.brokenAxis;t.forEach(function(t){i=h?.breakArray||[],s=e.isXAxis?e.min:a(n.options.threshold,e.min);let c=e?.options?.breaks?.filter(function(e){let t=!0;for(let s=0;s<i.length;s++){let o=i[s];if(o.from===e.from&&o.to===e.to){t=!1;break}}return t});d.forEach(function(n){o=a(n["stack"+t.toUpperCase()],n[t]),i.forEach(function(t){if(l(s)&&l(o)){let i="";s<t.from&&o>t.to||s>t.from&&o<t.from?i="pointBreak":(s<t.from&&o>t.from&&o<t.to||s>t.from&&o>t.to&&o<t.from)&&(i="pointInBreak"),i&&r(e,i,{point:n,brk:t})}}),c?.forEach(function(t){r(e,"pointOutsideOfBreak",{point:n,brk:t})})})})}}function g(){let t=this.currentDataGrouping,i=t?.gapSize,s=this.points.slice(),o=this.yAxis,r=this.options.gapSize,n=s.length-1;if(r&&n>0){let t,l;for("value"!==this.options.gapUnit&&(r*=this.basePointRange),i&&i>r&&i>=this.basePointRange&&(r=i);n--;)if(l&&!1!==l.visible||(l=s[n+1]),t=s[n],!1!==l.visible&&!1!==t.visible){if(l.x-t.x>r){let i=(t.x+l.x)/2;s.splice(n+1,0,{isNull:!0,x:i}),o.stacking&&this.options.stacking&&((o.stacking.stacks[this.stackKey][i]=new e(o,o.options.stackLabels,!1,i,this.stack)).total=0)}l=t}}return this.getGraphPath(s)}t.compose=function(e,t){if(!e.keepProps.includes("brokenAxis")){e.keepProps.push("brokenAxis"),s(e,"init",c),s(e,"afterInit",i),s(e,"afterSetTickPositions",h),s(e,"afterSetOptions",d);let o=t.prototype;o.drawBreaks=u,o.gappedPath=g,s(t,"afterGeneratePoints",p),s(t,"afterRender",f)}return e};class k{static isInBreak(e,t){let i=e.repeat||1/0,s=e.from,o=e.to-e.from,r=t>=s?(t-s)%i:i-(s-t)%i;return e.inclusive?r<=o:r<o&&0!==r}static lin2Val(e){let t=this.brokenAxis,i=t&&t.breakArray;if(!i||!l(e))return e;let s=e,o,r;for(r=0;r<i.length&&!((o=i[r]).from>=s);r++)o.to<s?s+=o.len:k.isInBreak(o,s)&&(s+=o.len);return s}static val2Lin(e){let t=this.brokenAxis,i=t&&t.breakArray;if(!i||!l(e))return e;let s=e,o,r;for(r=0;r<i.length;r++)if((o=i[r]).to<=e)s-=o.len;else if(o.from>=e)break;else if(k.isInBreak(o,e)){s-=e-o.from;break}return s}constructor(e){this.hasBreaks=!1,this.axis=e}findBreakAt(e,t){return o(t,function(t){return t.from<e&&e<t.to})}isInAnyBreak(e,t){let i=this.axis,s=i.options.breaks||[],o=s.length,r,n,d;if(o&&l(e)){for(;o--;)k.isInBreak(s[o],e)&&(r=!0,n||(n=a(s[o].showPoints,!i.isXAxis)));d=r&&t?r&&!n:r}return d}setBreaks(e,t){let i=this,s=i.axis,o=n(e)&&!!e.length&&!!Object.keys(e[0]).length;s.isDirty=i.hasBreaks!==o,i.hasBreaks=o,e!==s.options.breaks&&(s.options.breaks=s.userOptions.breaks=e),s.forceRedraw=!0,s.series.forEach(function(e){e.isDirty=!0}),o||s.val2lin!==k.val2Lin||(delete s.val2lin,delete s.lin2val),o&&(s.userOptions.ordinal=!1,s.lin2val=k.lin2Val,s.val2lin=k.val2Lin,s.setExtremes=function(e,t,o,r,n){if(i.hasBreaks){let s;let o=this.options.breaks||[];for(;s=i.findBreakAt(e,o);)e=s.to;for(;s=i.findBreakAt(t,o);)t=s.from;t<e&&(t=e)}s.constructor.prototype.setExtremes.call(this,e,t,o,r,n)},s.setAxisTranslation=function(){if(s.constructor.prototype.setAxisTranslation.call(this),i.unitLength=void 0,i.hasBreaks){let e=s.options.breaks||[],t=[],o=[],n=a(s.pointRangePadding,0),d=0,h,c,p=s.userMin||s.min,f=s.userMax||s.max,u,g;e.forEach(function(e){c=e.repeat||1/0,l(p)&&l(f)&&(k.isInBreak(e,p)&&(p+=e.to%c-p%c),k.isInBreak(e,f)&&(f-=f%c-e.from%c))}),e.forEach(function(e){if(u=e.from,c=e.repeat||1/0,l(p)&&l(f)){for(;u-c>p;)u-=c;for(;u<p;)u+=c;for(g=u;g<f;g+=c)t.push({value:g,move:"in"}),t.push({value:g+e.to-e.from,move:"out",size:e.breakSize})}}),t.sort(function(e,t){return e.value===t.value?("in"===e.move?0:1)-("in"===t.move?0:1):e.value-t.value}),h=0,u=p,t.forEach(function(e){1===(h+="in"===e.move?1:-1)&&"in"===e.move&&(u=e.value),0===h&&l(u)&&(o.push({from:u,to:e.value,len:e.value-u-(e.size||0)}),d+=e.value-u-(e.size||0))}),i.breakArray=o,l(p)&&l(f)&&l(s.min)&&(i.unitLength=f-p-d+n,r(s,"afterBreaks"),s.staticScale?s.transA=s.staticScale:i.unitLength&&(s.transA*=(f-s.min+n)/i.unitLength),n&&(s.minPixelPadding=s.transA*(s.minPointOffset||0)),s.min=p,s.max=f)}}),a(t,!0)&&s.chart.redraw()}}t.Additions=k}(i||(i={})),i}),i(t,"Core/Axis/GridAxis.js",[t["Core/Axis/Axis.js"],t["Core/Globals.js"],t["Core/Utilities.js"]],function(e,t,i){var s,o;let{dateFormats:r}=t,{addEvent:n,defined:l,erase:a,find:d,isArray:h,isNumber:c,merge:p,pick:f,timeUnits:u,wrap:g}=i;function k(e){return i.isObject(e,!0)}function m(e,t){let i={width:0,height:0};if(t.forEach(function(t){let s=e[t],o=0,r=0,n;k(s)&&(o=(n=k(s.label)?s.label:{}).getBBox?n.getBBox().height:0,n.textStr&&!c(n.textPxLength)&&(n.textPxLength=n.getBBox().width),r=c(n.textPxLength)?Math.round(n.textPxLength):0,n.textStr&&(r=Math.round(n.getBBox().width)),i.height=Math.max(o,i.height),i.width=Math.max(r,i.width))}),"treegrid"===this.options.type&&this.treeGrid&&this.treeGrid.mapOfPosToGridNode){let e=this.treeGrid.mapOfPosToGridNode[-1].height||0;i.width+=this.options.labels.indentation*(e-1)}return i}function x(e){let{grid:t}=this,i=3===this.side;if(i||e.apply(this),!t?.isColumn){let e=t?.columns||[];i&&(e=e.slice().reverse()),e.forEach(e=>{e.getOffset()})}i&&e.apply(this)}function b(e){if(!0===(this.options.grid||{}).enabled){let{axisTitle:t,height:i,horiz:o,left:r,offset:n,opposite:l,options:a,top:d,width:h}=this,c=this.tickSize(),p=t&&t.getBBox().width,u=a.title.x,g=a.title.y,k=f(a.title.margin,o?5:10),m=t?this.chart.renderer.fontMetrics(t).f:0,x=(o?d+i:r)+(o?1:-1)*(l?-1:1)*(c?c[0]/2:0)+(this.side===s.bottom?m:0);e.titlePosition.x=o?r-(p||0)/2-k+u:x+(l?h:0)+n+u,e.titlePosition.y=o?x-(l?i:0)+(l?m:-m)/2+n+g:d-k+g}}function y(){let{chart:t,options:{grid:i={}},userOptions:s}=this;if(i.enabled&&function(e){let t=e.options;t.labels.align=f(t.labels.align,"center"),e.categories||(t.showLastLabel=!1),e.labelRotation=0,t.labels.rotation=0,t.minTickInterval=1}(this),i.columns){let o=this.grid.columns=[],r=this.grid.columnIndex=0;for(;++r<i.columns.length;){let n=p(s,i.columns[r],{isInternal:!0,linkedTo:0,scrollbar:{enabled:!1}},{grid:{columns:void 0}}),l=new e(this.chart,n,"yAxis");l.grid.isColumn=!0,l.grid.columnIndex=r,a(t.axes,l),a(t[this.coll]||[],l),o.push(l)}}}function v(){let{axisTitle:e,grid:t,options:i}=this;if(!0===(i.grid||{}).enabled){let o=this.min||0,r=this.max||0,n=this.ticks[this.tickPositions[0]];if(e&&!this.chart.styledMode&&n?.slotWidth&&!this.options.title.style.width&&e.css({width:`${n.slotWidth}px`}),this.maxLabelDimensions=this.getMaxLabelDimensions(this.ticks,this.tickPositions),this.rightWall&&this.rightWall.destroy(),this.grid&&this.grid.isOuterAxis()&&this.axisLine){let e=i.lineWidth;if(e){let t=this.getLinePath(e),n=t[0],l=t[1],a=((this.tickSize("tick")||[1])[0]-1)*(this.side===s.top||this.side===s.left?-1:1);if("M"===n[0]&&"L"===l[0]&&(this.horiz?(n[2]+=a,l[2]+=a):(n[1]+=a,l[1]+=a)),!this.horiz&&this.chart.marginRight){let e=["L",this.left,n[2]||0],t=[n,e],s=["L",this.chart.chartWidth-this.chart.marginRight,this.toPixels(r+this.tickmarkOffset)],a=[["M",l[1]||0,this.toPixels(r+this.tickmarkOffset)],s];this.grid.upperBorder||o%1==0||(this.grid.upperBorder=this.grid.renderBorder(t)),this.grid.upperBorder&&(this.grid.upperBorder.attr({stroke:i.lineColor,"stroke-width":i.lineWidth}),this.grid.upperBorder.animate({d:t})),this.grid.lowerBorder||r%1==0||(this.grid.lowerBorder=this.grid.renderBorder(a)),this.grid.lowerBorder&&(this.grid.lowerBorder.attr({stroke:i.lineColor,"stroke-width":i.lineWidth}),this.grid.lowerBorder.animate({d:a}))}this.grid.axisLineExtra?(this.grid.axisLineExtra.attr({stroke:i.lineColor,"stroke-width":i.lineWidth}),this.grid.axisLineExtra.animate({d:t})):this.grid.axisLineExtra=this.grid.renderBorder(t),this.axisLine[this.showAxis?"show":"hide"]()}}if((t&&t.columns||[]).forEach(e=>e.render()),!this.horiz&&this.chart.hasRendered&&(this.scrollbar||this.linkedParent&&this.linkedParent.scrollbar)&&this.tickPositions.length){let e,t;let i=this.tickmarkOffset,s=this.tickPositions[this.tickPositions.length-1],n=this.tickPositions[0];for(;(e=this.hiddenLabels.pop())&&e.element;)e.show();for(;(t=this.hiddenMarks.pop())&&t.element;)t.show();(e=this.ticks[n].label)&&(o-n>i?this.hiddenLabels.push(e.hide()):e.show()),(e=this.ticks[s].label)&&(s-r>i?this.hiddenLabels.push(e.hide()):e.show());let l=this.ticks[s].mark;l&&s-r<i&&s-r>0&&this.ticks[s].isLast&&this.hiddenMarks.push(l.hide())}}}function P(){let e=this.tickPositions&&this.tickPositions.info,t=this.options,i=t.grid||{},s=this.userOptions.labels||{};i.enabled&&(this.horiz?(this.series.forEach(e=>{e.options.pointRange=0}),e&&t.dateTimeLabelFormats&&t.labels&&!l(s.align)&&(!1===t.dateTimeLabelFormats[e.unitName].range||e.count>1)&&(t.labels.align="left",l(s.x)||(t.labels.x=3))):"treegrid"!==this.options.type&&this.grid&&this.grid.columns&&(this.minPointOffset=this.tickInterval))}function G(e){let t;let i=this.options,s=e.userOptions,o=i&&k(i.grid)?i.grid:{};!0===o.enabled&&(t=p(!0,{className:"highcharts-grid-axis "+(s.className||""),dateTimeLabelFormats:{hour:{list:["%H:%M","%H"]},day:{list:["%A, %e. %B","%a, %e. %b","%E"]},week:{list:["Week %W","W%W"]},month:{list:["%B","%b","%o"]}},grid:{borderWidth:1},labels:{padding:2,style:{fontSize:"0.9em"}},margin:0,title:{text:null,reserveSpace:!1,rotation:0,style:{textOverflow:"ellipsis"}},units:[["millisecond",[1,10,100]],["second",[1,10]],["minute",[1,5,15]],["hour",[1,6]],["day",[1]],["week",[1]],["month",[1]],["year",null]]},s),"xAxis"!==this.coll||(l(s.linkedTo)&&!l(s.tickPixelInterval)&&(t.tickPixelInterval=350),!(!l(s.tickPixelInterval)&&l(s.linkedTo))||l(s.tickPositioner)||l(s.tickInterval)||l(s.units)||(t.tickPositioner=function(e,i){let s=this.linkedParent&&this.linkedParent.tickPositions&&this.linkedParent.tickPositions.info;if(s){let o=t.units||[],r,n=1,l="year";for(let e=0;e<o.length;e++){let t=o[e];if(t&&t[0]===s.unitName){r=e;break}}let a=c(r)&&o[r+1];if(a){l=a[0]||"year";let e=a[1];n=e&&e[0]||1}else"year"===s.unitName&&(n=10*s.count);let d=u[l];return this.tickInterval=d*n,this.chart.time.getTimeTicks({unitRange:d,count:n,unitName:l},e,i,this.options.startOfWeek)}})),p(!0,this.options,t),this.horiz&&(i.minPadding=f(s.minPadding,0),i.maxPadding=f(s.maxPadding,0)),c(i.grid.borderWidth)&&(i.tickWidth=i.lineWidth=o.borderWidth))}function A(e){let t=e.userOptions,i=t&&t.grid||{},s=i.columns;i.enabled&&s&&p(!0,this.options,s[0])}function T(){(this.grid.columns||[]).forEach(e=>e.setScale())}function C(e){let{horiz:t,maxLabelDimensions:i,options:{grid:s={}}}=this;if(s.enabled&&i){let o=2*this.options.labels.distance,r=t?s.cellHeight||o+i.height:o+i.width;h(e.tickSize)?e.tickSize[0]=r:e.tickSize=[r,0]}}function B(){this.axes.forEach(e=>{(e.grid&&e.grid.columns||[]).forEach(e=>{e.setAxisSize(),e.setAxisTranslation()})})}function O(e){let{grid:t}=this;(t.columns||[]).forEach(t=>t.destroy(e.keepEvents)),t.columns=void 0}function w(e){let t=e.userOptions||{},i=t.grid||{};i.enabled&&l(i.borderColor)&&(t.tickColor=t.lineColor=i.borderColor),this.grid||(this.grid=new M(this)),this.hiddenLabels=[],this.hiddenMarks=[]}function I(e){let t=this.label,i=this.axis,o=i.reversed,r=i.chart,n=i.options.grid||{},l=i.options.labels,a=l.align,d=s[i.side],h=e.tickmarkOffset,p=i.tickPositions,f=this.pos-h,u=c(p[e.index+1])?p[e.index+1]-h:(i.max||0)+h,g=i.tickSize("tick"),k=g?g[0]:0,m=g?g[1]/2:0;if(!0===n.enabled){let s,n,h,c;if("top"===d?n=(s=i.top+i.offset)-k:"bottom"===d?s=(n=r.chartHeight-i.bottom+i.offset)+k:(s=i.top+i.len-(i.translate(o?u:f)||0),n=i.top+i.len-(i.translate(o?f:u)||0)),"right"===d?c=(h=r.chartWidth-i.right+i.offset)+k:"left"===d?h=(c=i.left+i.offset)-k:(h=Math.round(i.left+(i.translate(o?u:f)||0))-m,c=Math.min(Math.round(i.left+(i.translate(o?f:u)||0))-m,i.left+i.len)),this.slotWidth=c-h,e.pos.x="left"===a?h:"right"===a?c:h+(c-h)/2,e.pos.y=n+(s-n)/2,t){let i=r.renderer.fontMetrics(t),s=t.getBBox().height;if(l.useHTML)e.pos.y+=i.b+-(s/2);else{let t=Math.round(s/i.h);e.pos.y+=(i.b-(i.h-i.f))/2+-((t-1)*i.h/2)}}e.pos.x+=i.horiz&&l.x||0}}function E(e){let{axis:i,value:s}=e;if(i.options.grid&&i.options.grid.enabled){let o;let r=i.tickPositions,n=(i.linkedParent||i).series[0],l=s===r[0],a=s===r[r.length-1],h=n&&d(n.options.data,function(e){return e[i.isXAxis?"x":"y"]===s});h&&n.is("gantt")&&(o=p(h),t.seriesTypes.gantt.prototype.pointClass.setGanttPointAliases(o)),e.isFirst=l,e.isLast=a,e.point=o}}function N(){let e=this.options,t=e.grid||{},i=this.categories,s=this.tickPositions,o=s[0],r=s[1],n=s[s.length-1],l=s[s.length-2],a=this.linkedParent&&this.linkedParent.min,d=this.linkedParent&&this.linkedParent.max,h=a||this.min,p=d||this.max,f=this.tickInterval,u=c(h)&&h>=o+f&&h<r,g=c(h)&&o<h&&o+f>h,k=c(p)&&n>p&&n-f<p,m=c(p)&&p<=n-f&&p>l;!0===t.enabled&&!i&&(this.isXAxis||this.isLinked)&&((g||u)&&!e.startOnTick&&(s[0]=h),(k||m)&&!e.endOnTick&&(s[s.length-1]=p))}function L(e){var t;let{options:{grid:i={}}}=this;return!0===i.enabled&&this.categories?this.tickInterval:e.apply(this,(t=arguments,Array.prototype.slice.call(t,1)))}(o=s||(s={}))[o.top=0]="top",o[o.right=1]="right",o[o.bottom=2]="bottom",o[o.left=3]="left";class M{constructor(e){this.axis=e}isOuterAxis(){let e=this.axis,t=e.chart,i=e.grid.columnIndex,s=e.linkedParent?.grid.columns||e.grid.columns||[],o=i?e.linkedParent:e,r=-1,n=0;return 3===e.side&&!t.inverted&&s.length?!e.linkedParent:((t[e.coll]||[]).forEach((t,i)=>{t.side!==e.side||t.options.isInternal||(n=i,t!==o||(r=i))}),n===r&&(!c(i)||s.length===i))}renderBorder(e){let t=this.axis,i=t.chart.renderer,s=t.options,o=i.path(e).addClass("highcharts-axis-line").add(t.axisGroup);return i.styledMode||o.attr({stroke:s.lineColor,"stroke-width":s.lineWidth,zIndex:7}),o}}return r.E=function(e){return this.dateFormat("%a",e,!0).charAt(0)},r.W=function(e){let t=this,i=new this.Date(e);["Hours","Milliseconds","Minutes","Seconds"].forEach(function(e){t.set(e,i,0)});let s=(this.get("Day",i)+6)%7,o=new this.Date(i.valueOf());this.set("Date",o,this.get("Date",i)-s+3);let r=new this.Date(this.get("FullYear",o),0,1);return 4!==this.get("Day",r)&&(this.set("Month",i,0),this.set("Date",i,1+(11-this.get("Day",r))%7)),(1+Math.floor((o.valueOf()-r.valueOf())/6048e5)).toString()},{compose:function(e,t,i){return e.keepProps.includes("grid")||(e.keepProps.push("grid"),e.prototype.getMaxLabelDimensions=m,g(e.prototype,"unsquish",L),g(e.prototype,"getOffset",x),n(e,"init",w),n(e,"afterGetTitlePosition",b),n(e,"afterInit",y),n(e,"afterRender",v),n(e,"afterSetAxisTranslation",P),n(e,"afterSetOptions",G),n(e,"afterSetOptions",A),n(e,"afterSetScale",T),n(e,"afterTickSize",C),n(e,"trimTicks",N),n(e,"destroy",O),n(t,"afterSetChartSize",B),n(i,"afterGetLabelPosition",I),n(i,"labelFormat",E)),e}}}),i(t,"Gantt/Tree.js",[t["Core/Utilities.js"]],function(e){let{extend:t,isNumber:i,pick:s}=e;function o(e,r,n,l,a,d){let h=d&&d.after,c=d&&d.before,p={data:l,depth:n-1,id:e,level:n,parent:r||""},f=0,u=0,g,k;"function"==typeof c&&c(p,d);let m=(a[e]||[]).map(t=>{let s=o(t.id,e,n+1,t,a,d),r=t.start||NaN,l=!0===t.milestone?r:t.end||NaN;return g=!i(g)||r<g?r:g,k=!i(k)||l>k?l:k,f=f+1+s.descendants,u=Math.max(s.height+1,u),s});return l&&(l.start=s(l.start,g),l.end=s(l.end,k)),t(p,{children:m,descendants:f,height:u}),"function"==typeof h&&h(p,d),p}return{getNode:o,getTree:function(e,t){return o("",null,1,null,function(e){let t=[],i=e.reduce((e,i)=>{let{parent:s="",id:o}=i;return void 0===e[s]&&(e[s]=[]),e[s].push(i),o&&t.push(o),e},{});return Object.keys(i).forEach(e=>{if(""!==e&&-1===t.indexOf(e)){let t=i[e].map(function(e){let{...t}=e;return t});i[""].push(...t),delete i[e]}}),i}(e),t)}}}),i(t,"Core/Axis/TreeGrid/TreeGridTick.js",[t["Core/Utilities.js"]],function(e){let{addEvent:t,removeEvent:i,isObject:s,isNumber:o,pick:r,wrap:n}=e;function l(){this.treeGrid||(this.treeGrid=new h(this))}function a(e,t,i,n,l,a,d,h,c){let p,f,u;let g=r(this.options&&this.options.labels,a),k=this.pos,m=this.axis,x="treegrid"===m.options.type,b=e.apply(this,[t,i,n,l,g,d,h,c]);if(x){let{width:e=0,padding:t=m.linkedParent?0:5}=g&&s(g.symbol,!0)?g.symbol:{},i=g&&o(g.indentation)?g.indentation:0;u=(f=(p=m.treeGrid.mapOfPosToGridNode)&&p[k])&&f.depth||1,b.x+=e+2*t+(u-1)*i}return b}function d(e){let n,l,a;let{pos:d,axis:h,label:c,treeGrid:p,options:f}=this,u=p?.labelIcon,g=c?.element,{treeGrid:k,options:m,chart:x,tickPositions:b}=h,y=k.mapOfPosToGridNode,v=r(f?.labels,m?.labels),P=v&&s(v.symbol,!0)?v.symbol:{},G=y&&y[d],{descendants:A,depth:T}=G||{},C=G&&A&&A>0,B="treegrid"===m.type&&g,O=b.indexOf(d)>-1,w="highcharts-treegrid-node-",I=w+"level-",E=x.styledMode;B&&G&&c.removeClass(RegExp(I+".*")).addClass(I+T),e.apply(this,Array.prototype.slice.call(arguments,1)),B&&C?(n=k.isCollapsed(G),function(e,t){let i=e.treeGrid,s=!i.labelIcon,n=t.renderer,l=t.xy,a=t.options,d=a.width||0,h=a.height||0,c=a.padding??e.axis.linkedParent?0:5,p={x:l.x-d/2-c,y:l.y-h/2},f=t.collapsed?90:180,u=t.show&&o(p.y),g=i.labelIcon;g||(i.labelIcon=g=n.path(n.symbols[a.type](a.x||0,a.y||0,d,h)).addClass("highcharts-label-icon").add(t.group)),g[u?"show":"hide"](),n.styledMode||g.attr({cursor:"pointer",fill:r(t.color,"#666666"),"stroke-width":1,stroke:a.lineColor,strokeWidth:a.lineWidth||0}),g[s?"attr":"animate"]({translateX:p.x,translateY:p.y,rotation:f})}(this,{color:!E&&c.styles.color||"",collapsed:n,group:c.parentGroup,options:P,renderer:c.renderer,show:O,xy:c.xy}),l=w+(n?"collapsed":"expanded"),a=w+(n?"expanded":"collapsed"),c.addClass(l).removeClass(a),E||c.css({cursor:"pointer"}),[c,u].forEach(e=>{e&&!e.attachedTreeGridEvents&&(t(e.element,"mouseover",function(){c.addClass("highcharts-treegrid-node-active"),c.renderer.styledMode||c.css({textDecoration:"underline"})}),t(e.element,"mouseout",function(){!function(e,t){let i=s(t.style)?t.style:{};e.removeClass("highcharts-treegrid-node-active"),e.renderer.styledMode||e.css({textDecoration:i.textDecoration||"none"})}(c,v)}),t(e.element,"click",function(){p.toggleCollapse()}),e.attachedTreeGridEvents=!0)})):u&&(i(g),c?.css({cursor:"default"}),u.destroy())}class h{static compose(e){let i=e.prototype;i.toggleCollapse||(t(e,"init",l),n(i,"getLabelPosition",a),n(i,"renderLabel",d),i.collapse=function(e){this.treeGrid.collapse(e)},i.expand=function(e){this.treeGrid.expand(e)},i.toggleCollapse=function(e){this.treeGrid.toggleCollapse(e)})}constructor(e){this.tick=e}collapse(e){let t=this.tick,i=t.axis,s=i.brokenAxis;if(s&&i.treeGrid.mapOfPosToGridNode){let o=t.pos,n=i.treeGrid.mapOfPosToGridNode[o],l=i.treeGrid.collapse(n);s.setBreaks(l,r(e,!0))}}destroy(){this.labelIcon&&this.labelIcon.destroy()}expand(e){let{pos:t,axis:i}=this.tick,{treeGrid:s,brokenAxis:o}=i,n=s.mapOfPosToGridNode;if(o&&n){let i=n[t],l=s.expand(i);o.setBreaks(l,r(e,!0))}}toggleCollapse(e){let t=this.tick,i=t.axis,s=i.brokenAxis;if(s&&i.treeGrid.mapOfPosToGridNode){let o=t.pos,n=i.treeGrid.mapOfPosToGridNode[o],l=i.treeGrid.toggleCollapse(n);s.setBreaks(l,r(e,!0))}}}return h}),i(t,"Series/TreeUtilities.js",[t["Core/Color/Color.js"],t["Core/Utilities.js"]],function(e,t){let{extend:i,isArray:s,isNumber:o,isObject:r,merge:n,pick:l,relativeLength:a}=t;return{getColor:function(t,i){let s,o,r,n,a,d;let h=i.index,c=i.mapOptionsToLevel,p=i.parentColor,f=i.parentColorIndex,u=i.series,g=i.colors,k=i.siblings,m=u.points,x=u.chart.options.chart;return t&&(s=m[t.i],o=c[t.level]||{},s&&o.colorByPoint&&(n=s.index%(g?g.length:x.colorCount),r=g&&g[n]),u.chart.styledMode||(a=l(s&&s.options.color,o&&o.color,r,p&&(t=>{let i=o&&o.colorVariation;return i&&"brightness"===i.key&&h&&k?e.parse(t).brighten(i.to*(h/k)).get():t})(p),u.color)),d=l(s&&s.options.colorIndex,o&&o.colorIndex,n,f,i.colorIndex)),{color:a,colorIndex:d}},getLevelOptions:function(e){let t,i,a,d,h,c;let p={};if(r(e))for(d=o(e.from)?e.from:1,c=e.levels,i={},t=r(e.defaults)?e.defaults:{},s(c)&&(i=c.reduce((e,i)=>{let s,a,h;return r(i)&&o(i.level)&&(a=l((h=n({},i)).levelIsConstant,t.levelIsConstant),delete h.levelIsConstant,delete h.level,r(e[s=i.level+(a?0:d-1)])?n(!0,e[s],h):e[s]=h),e},{})),h=o(e.to)?e.to:1,a=0;a<=h;a++)p[a]=n({},t,r(i[a])?i[a]:{});return p},getNodeWidth:function(e,t){let{chart:i,options:s}=e,{nodeDistance:o=0,nodeWidth:r=0}=s,{plotSizeX:n=1}=i;if("auto"===r){if("string"==typeof o&&/%$/.test(o))return n/(t+parseFloat(o)/100*(t-1));let e=Number(o);return(n+e)/(t||1)-e}return a(r,n)},setTreeValues:function e(t,s){let o=s.before,r=s.idRoot,n=s.mapIdToNode[r],a=!1!==s.levelIsConstant,d=s.points[t.i],h=d&&d.options||{},c=[],p=0;t.levelDynamic=t.level-(a?0:n.level),t.name=l(d&&d.name,""),t.visible=r===t.id||!0===s.visible,"function"==typeof o&&(t=o(t,s)),t.children.forEach((o,r)=>{let n=i({},s);i(n,{index:r,siblings:t.children.length,visible:t.visible}),o=e(o,n),c.push(o),o.visible&&(p+=o.val)});let f=l(h.value,p);return t.visible=f>=0&&(p>0||t.visible),t.children=c,t.childrenTotal=p,t.isLeaf=t.visible&&!p,t.val=f,t},updateRootId:function(e){let t,i;return r(e)&&(i=r(e.options)?e.options:{},t=l(e.rootNode,i.rootId,""),r(e.userOptions)&&(e.userOptions.rootId=t),e.rootNode=t),t}}}),i(t,"Core/Axis/TreeGrid/TreeGridAxis.js",[t["Core/Axis/BrokenAxis.js"],t["Core/Axis/GridAxis.js"],t["Gantt/Tree.js"],t["Core/Axis/TreeGrid/TreeGridTick.js"],t["Series/TreeUtilities.js"],t["Core/Utilities.js"]],function(e,t,i,s,o,r){let n;let{getLevelOptions:l}=o,{addEvent:a,find:d,fireEvent:h,isArray:c,isObject:p,isString:f,merge:u,pick:g,removeEvent:k,wrap:m}=r;function x(e,t){let i=e.collapseEnd||0,s=e.collapseStart||0;return i>=t&&(s-=.5),{from:s,to:i,showPoints:!1}}function b(e,t,s){let o=[],r=[],n={},l="boolean"==typeof t&&t,a={},h=-1,c=i.getTree(e,{after:function(e){let t=a[e.pos],i=0,s=0;t.children.forEach(function(e){s+=(e.descendants||0)+1,i=Math.max((e.height||0)+1,i)}),t.descendants=s,t.height=i,t.collapsed&&r.push(t)},before:function(e){let t,i;let s=p(e.data,!0)?e.data:{},r=f(s.name)?s.name:"",c=n[e.parent],u=p(c,!0)?a[c.pos]:null;l&&p(u,!0)&&(t=d(u.children,function(e){return e.name===r}))?(i=t.pos,t.nodes.push(e)):i=h++,!a[i]&&(a[i]=t={depth:u?u.depth+1:0,name:r,id:s.id,nodes:[e],children:[],pos:i},-1!==i&&o.push(r),p(u,!0)&&u.children.push(t)),f(e.id)&&(n[e.id]=e),t&&!0===s.collapsed&&(t.collapsed=!0),e.pos=i}});return{categories:o,mapOfIdToNode:n,mapOfPosToGridNode:a=function(e,t){let i=function(e,s,o){let r=e.nodes,n=s+(-1===s?0:t-1),l=(n-s)/2,a=s+l;return r.forEach(function(e){let t=e.data;p(t,!0)&&(t.y=s+(t.seriesIndex||0),delete t.seriesIndex),e.pos=a}),o[a]=e,e.pos=a,e.tickmarkOffset=l+.5,e.collapseStart=n+.5,e.children.forEach(function(e){i(e,n+1,o),n=(e.collapseEnd||0)-.5}),e.collapseEnd=n+.5,o};return i(e["-1"],-1,{})}(a,s),collapsedNodes:r,tree:c}}function y(e){e.target.axes.filter(function(e){return"treegrid"===e.options.type}).forEach(function(t){let i=t.options||{},s=i.labels,o=i.uniqueNames,r=i.max,n=!t.treeGrid.mapOfPosToGridNode||t.series.some(function(e){return!e.hasRendered||e.isDirtyData||e.isDirty}),a=0,d,h;if(n){if(d=t.series.reduce(function(e,t){return t.visible&&((t.options.data||[]).forEach(function(i){t.options.keys&&t.options.keys.length&&(i=t.pointClass.prototype.optionsToObject.call({series:t},i),t.pointClass.setGanttPointAliases(i)),p(i,!0)&&(i.seriesIndex=a,e.push(i))}),!0===o&&a++),e},[]),r&&d.length<r)for(let e=d.length;e<=r;e++)d.push({name:e+"​"});h=b(d,o||!1,!0===o?a:1),t.categories=h.categories,t.treeGrid.mapOfPosToGridNode=h.mapOfPosToGridNode,t.hasNames=!0,t.treeGrid.tree=h.tree,t.series.forEach(function(e){let t=(e.options.data||[]).map(function(t){return c(t)&&e.options.keys&&e.options.keys.length&&d.forEach(function(e){t.indexOf(e.x)>=0&&t.indexOf(e.x2)>=0&&(t=e)}),p(t,!0)?u(t):t});e.visible&&e.setData(t,!1)}),t.treeGrid.mapOptionsToLevel=l({defaults:s,from:1,levels:s&&s.levels,to:t.treeGrid.tree&&t.treeGrid.tree.height}),"beforeRender"===e.type&&(t.treeGrid.collapsedNodes=h.collapsedNodes)}})}function v(e,t){let i=this.treeGrid.mapOptionsToLevel||{},s="treegrid"===this.options.type,o=this.ticks,r=o[t],l,a,d;s&&this.treeGrid.mapOfPosToGridNode?((l=i[(d=this.treeGrid.mapOfPosToGridNode[t]).depth])&&(a={labels:l}),!r&&n?o[t]=r=new n(this,t,void 0,void 0,{category:d.name,tickmarkOffset:d.tickmarkOffset,options:a}):(r.parameters.category=d.name,r.options=a,r.addLabel())):e.apply(this,Array.prototype.slice.call(arguments,1))}function P(e,t,i,s){let o=this,r="treegrid"===i.type;o.treeGrid||(o.treeGrid=new T(o)),r&&(a(t,"beforeRender",y),a(t,"beforeRedraw",y),a(t,"addSeries",function(e){if(e.options.data){let t=b(e.options.data,i.uniqueNames||!1,1);o.treeGrid.collapsedNodes=(o.treeGrid.collapsedNodes||[]).concat(t.collapsedNodes)}}),a(o,"foundExtremes",function(){o.treeGrid.collapsedNodes&&o.treeGrid.collapsedNodes.forEach(function(e){let t=o.treeGrid.collapse(e);o.brokenAxis&&(o.brokenAxis.setBreaks(t,!1),o.treeGrid.collapsedNodes&&(o.treeGrid.collapsedNodes=o.treeGrid.collapsedNodes.filter(t=>e.collapseStart!==t.collapseStart||e.collapseEnd!==t.collapseEnd)))})}),a(o,"afterBreaks",function(){"yAxis"===o.coll&&!o.staticScale&&o.chart.options.chart.height&&(o.isDirty=!0)}),i=u({grid:{enabled:!0},labels:{align:"left",levels:[{level:void 0},{level:1,style:{fontWeight:"bold"}}],symbol:{type:"triangle",x:-5,y:-5,height:10,width:10}},uniqueNames:!1},i,{reversed:!0})),e.apply(o,[t,i,s]),r&&(o.hasNames=!0,o.options.showLastLabel=!0)}function G(e){let t=this.options,i="number"==typeof t.linkedTo?this.chart[this.coll]?.[t.linkedTo]:void 0;if("treegrid"===t.type){if(this.min=g(this.userMin,t.min,this.dataMin),this.max=g(this.userMax,t.max,this.dataMax),h(this,"foundExtremes"),this.setAxisTranslation(),this.tickInterval=1,this.tickmarkOffset=.5,this.tickPositions=this.treeGrid.mapOfPosToGridNode?this.treeGrid.getTickPositions():[],i){let e=i.getExtremes();this.min=g(e.min,e.dataMin),this.max=g(e.max,e.dataMax),this.tickPositions=i.tickPositions}this.linkedParent=i}else e.apply(this,Array.prototype.slice.call(arguments,1))}function A(e){let t=this;"treegrid"===t.options.type&&t.visible&&t.tickPositions.forEach(function(e){let i=t.ticks[e];i.label&&i.label.attachedTreeGridEvents&&(k(i.label.element),i.label.attachedTreeGridEvents=!1)}),e.apply(t,Array.prototype.slice.call(arguments,1))}class T{static compose(o,r,l,a){if(!o.keepProps.includes("treeGrid")){let e=o.prototype;o.keepProps.push("treeGrid"),m(e,"generateTick",v),m(e,"init",P),m(e,"setTickInterval",G),m(e,"redraw",A),e.utils={getNode:i.getNode},n||(n=a)}return t.compose(o,r,a),e.compose(o,l),s.compose(a),o}constructor(e){this.axis=e}setCollapsedStatus(e){let t=this.axis,i=t.chart;t.series.forEach(function(t){let s=t.options.data;if(e.id&&s){let o=i.get(e.id),r=s[t.data.indexOf(o)];o&&r&&(o.collapsed=e.collapsed,r.collapsed=e.collapsed)}})}collapse(e){let t=this.axis,i=t.options.breaks||[],s=x(e,t.max);return i.push(s),e.collapsed=!0,t.treeGrid.setCollapsedStatus(e),i}expand(e){let t=this.axis,i=t.options.breaks||[],s=x(e,t.max);return e.collapsed=!1,t.treeGrid.setCollapsedStatus(e),i.reduce(function(e,t){return(t.to!==s.to||t.from!==s.from)&&e.push(t),e},[])}getTickPositions(){let e=this.axis,t=Math.floor(e.min/e.tickInterval)*e.tickInterval,i=Math.ceil(e.max/e.tickInterval)*e.tickInterval;return Object.keys(e.treeGrid.mapOfPosToGridNode||{}).reduce(function(s,o){let r=+o;return r>=t&&r<=i&&!(e.brokenAxis&&e.brokenAxis.isInAnyBreak(r))&&s.push(r),s},[])}isCollapsed(e){let t=this.axis,i=t.options.breaks||[],s=x(e,t.max);return i.some(function(e){return e.from===s.from&&e.to===s.to})}toggleCollapse(e){return this.isCollapsed(e)?this.expand(e):this.collapse(e)}}return T}),i(t,"masters/modules/treegrid.src.js",[t["Core/Globals.js"],t["Core/Axis/TreeGrid/TreeGridAxis.js"]],function(e,t){return t.compose(e.Axis,e.Chart,e.Series,e.Tick),e})});