(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-6a0fb1a4"],{"129f":function(t,e){t.exports=Object.is||function(t,e){return t===e?0!==t||1/t===1/e:t!=t&&e!=e}},"159b":function(t,e,a){var n=a("da84"),r=a("fdbc"),s=a("785a"),i=a("17c2"),c=a("9112"),o=function(t){if(t&&t.forEach!==i)try{c(t,"forEach",i)}catch(e){t.forEach=i}};for(var l in r)r[l]&&o(n[l]&&n[l].prototype);o(s)},"17c2":function(t,e,a){"use strict";var n=a("b727").forEach,r=a("a640"),s=r("forEach");t.exports=s?[].forEach:function(t){return n(this,t,arguments.length>1?arguments[1]:void 0)}},5530:function(t,e,a){"use strict";a.d(e,"a",(function(){return s}));a("b64b"),a("a4d3"),a("4de4"),a("e439"),a("159b"),a("dbb4");var n=a("ade3");function r(t,e){var a=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),a.push.apply(a,n)}return a}function s(t){for(var e=1;e<arguments.length;e++){var a=null!=arguments[e]?arguments[e]:{};e%2?r(Object(a),!0).forEach((function(e){Object(n["a"])(t,e,a[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(a)):r(Object(a)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(a,e))}))}return t}},"841c":function(t,e,a){"use strict";var n=a("d784"),r=a("825a"),s=a("1d80"),i=a("129f"),c=a("577e"),o=a("dc4a"),l=a("14c3");n("search",(function(t,e,a){return[function(e){var a=s(this),n=void 0==e?void 0:o(e,t);return n?n.call(e,a):new RegExp(e)[t](c(a))},function(t){var n=r(this),s=c(t),o=a(e,n,s);if(o.done)return o.value;var u=n.lastIndex;i(u,0)||(n.lastIndex=0);var f=l(n,s);return i(n.lastIndex,u)||(n.lastIndex=u),null===f?-1:f.index}]}))},ade3:function(t,e,a){"use strict";function n(t,e,a){return e in t?Object.defineProperty(t,e,{value:a,enumerable:!0,configurable:!0,writable:!0}):t[e]=a,t}a.d(e,"a",(function(){return n}))},b456:function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-form-group",{attrs:{label:t.label,"label-for":"tags-with-dropdown"}},[a("b-form-tags",{staticClass:"mb-2",attrs:{id:"tags-with-dropdown","no-outer-focus":""},scopedSlots:t._u([{key:"default",fn:function(e){var n=e.tags,r=e.disabled,s=e.addTag,i=e.removeTag;return[n.length>0?a("ul",{staticClass:"list-inline d-inline-block mb-2",staticStyle:{"max-width":"100%"}},t._l(n,(function(e){return a("li",{staticClass:"list-inline-item",staticStyle:{"max-width":"100%"}},[a("b-form-tag",{attrs:{title:JSON.parse(e).name,disabled:r,variant:"info"},on:{remove:function(t){return i(e)}}},[t._v(t._s(JSON.parse(e).name))])],1)})),0):t._e(),a("b-dropdown",{staticClass:"filter-dropdown",attrs:{size:"sm",variant:"outline-secondary",block:"","menu-class":"w-100"},scopedSlots:t._u([{key:"button-content",fn:function(){return[a("i",{staticClass:"flaticon-tags"}),t._v(" Choose tags ")]},proxy:!0}],null,!0)},[a("b-dropdown-form",{on:{submit:function(t){return t.stopPropagation(),t.preventDefault(),function(){}.apply(null,arguments)}}},[a("b-form-group",{staticClass:"mb-0 mt-3",attrs:{label:"Search tags","label-for":"tag-search-input","label-cols-md":"auto","label-size":"sm",description:t.search_desc,disabled:r}},[a("b-input-group",[a("b-form-input",{attrs:{id:"tag-search-input",type:"search",size:"sm",placeholder:"Enter a tag name and press Enter to create a new tag",autocomplete:"off"},nativeOn:{keydown:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.add_new_tag.apply(null,arguments)}},model:{value:t.search,callback:function(e){t.search="string"===typeof e?e.trim():e},expression:"search"}})],1)],1)],1),a("b-dropdown-divider"),a("vue-perfect-scrollbar",{staticClass:"filter-items",attrs:{settings:{suppressScrollX:!1,wheelPropagation:!1}}},t._l(t.available_tags,(function(e,n){return a("b-dropdown-item-button",{key:n,on:{click:function(a){return t.on_tag_click({tag:e,addTag:s})}}},[t._v(" "+t._s(e.name)+" ")])})),1)],1)]}}]),model:{value:t.selectedTags,callback:function(e){t.selectedTags=e},expression:"selectedTags"}})],1)},r=[],s=a("5530"),i=a("b85c"),c=(a("b0c0"),a("ac1f"),a("841c"),a("498a"),a("7db0"),a("4de4"),a("c740"),a("2f62")),o={props:{tag_type:"",label:"",selected_tags:[],on_change:null},data:function(){return{selectedTags:this.selected_tags,search:""}},watch:{selected_tags:{handler:function(){this.selectedTags=Array.isArray(this.selected_tags)?this.selected_tags:[]},immediate:!0},selectedTags:{handler:function(){var t,e=[],a=Object(i["a"])(this.selectedTags);try{for(a.s();!(t=a.n()).done;){var n=t.value;"string"===typeof n&&(n=JSON.parse(n)),e.push({name:n.name,id:n.id})}}catch(r){a.e(r)}finally{a.f()}"function"===typeof this.on_change&&this.on_change(e)},immediate:!0,deep:!0}},methods:{on_tag_click:function(t){var e=t.tag,a=t.addTag;a(JSON.stringify(e)),this.search=""},add_new_tag:function(){if(""!==this.search.trim()){var t=this.search.trim().toLowerCase(),e=this.selectedTags.find((function(e){return e="string"===typeof e?JSON.parse(e):e,e.name.trim().toLowerCase()===t}));if(e)return void(this.search="");var a=this.all_tags.find((function(e){return e.name.trim().toLowerCase()===t}));if(a)return this.selectedTags.push(JSON.stringify(a)),void(this.search="");this.selectedTags.push(JSON.stringify({name:this.search})),this.search=""}}},computed:Object(s["a"])(Object(s["a"])({},Object(c["d"])({contact_tags:function(t){return t.global.tags},template_tags:function(t){return t.emailAI.tags}})),{},{all_tags:function(){var t;return t="template_tags"===this.tag_type?this.template_tags:this.contact_tags,Array.isArray(t)?t:[]},available_tags:function(){var t=this,e=this.search.trim().toLowerCase(),a=this.all_tags.filter((function(e){return-1===t.selectedTags.findIndex((function(t){return("string"===typeof t?JSON.parse(t):t).name===e.name}))}));return e?a.filter((function(t){return t.name.toLowerCase().indexOf(e)>-1})):a},search_desc:function(){return this.search.trim().toLowerCase()&&0===this.available_tags.length?"No matching tags. Press Enter to add it":""}})},l=o,u=a("2877"),f=Object(u["a"])(l,n,r,!1,null,null,null);e["default"]=f.exports},dbb4:function(t,e,a){var n=a("23e7"),r=a("83ab"),s=a("56ef"),i=a("fc6a"),c=a("06cf"),o=a("8418");n({target:"Object",stat:!0,sham:!r},{getOwnPropertyDescriptors:function(t){var e,a,n=i(t),r=c.f,l=s(n),u={},f=0;while(l.length>f)a=r(n,e=l[f++]),void 0!==a&&o(u,e,a);return u}})},e439:function(t,e,a){var n=a("23e7"),r=a("d039"),s=a("fc6a"),i=a("06cf").f,c=a("83ab"),o=r((function(){i(1)})),l=!c||o;n({target:"Object",stat:!0,forced:l,sham:!c},{getOwnPropertyDescriptor:function(t,e){return i(s(t),e)}})}}]);