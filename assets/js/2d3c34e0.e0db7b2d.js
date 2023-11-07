"use strict";(self.webpackChunkbadger_home=self.webpackChunkbadger_home||[]).push([[9280],{9307:(e,n,i)=>{i.r(n),i.d(n,{assets:()=>l,contentTitle:()=>s,default:()=>h,frontMatter:()=>r,metadata:()=>a,toc:()=>c});var t=i(5893),o=i(1151);const r={sidebar_position:1},s="Introduction",a={id:"intro",title:"Introduction",description:"Badger is an optimizer specifically designed for Accelerator Control Room (ACR). It's the spiritual successor of Ocelot optimizer.",source:"@site/versioned_docs/version-0.11/intro.md",sourceDirName:".",slug:"/intro",permalink:"/Badger/docs/intro",draft:!1,unlisted:!1,editUrl:"https://github.com/SLAC-ML/Badger-Home/edit/master/versioned_docs/version-0.11/intro.md",tags:[],version:"0.11",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",next:{title:"Installation",permalink:"/Badger/docs/getting-started/installation"}},l={},c=[{value:"Important concepts",id:"important-concepts",level:2},{value:"Routine",id:"routine",level:3},{value:"Interface",id:"interface",level:3},{value:"Environment",id:"environment",level:3},{value:"Routine config",id:"routine-config",level:3},{value:"Features",id:"features",level:2},{value:"Plugin system",id:"plugin-system",level:3},{value:"Extension system",id:"extension-system",level:3}];function d(e){const n={a:"a",admonition:"admonition",code:"code",h1:"h1",h2:"h2",h3:"h3",img:"img",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,o.a)(),...e.components};return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(n.h1,{id:"introduction",children:"Introduction"}),"\n",(0,t.jsxs)(n.p,{children:["Badger is an optimizer specifically designed for Accelerator Control Room (ACR). It's the spiritual successor of ",(0,t.jsx)(n.a,{href:"https://github.com/ocelot-collab/optimizer",children:"Ocelot optimizer"}),"."]}),"\n",(0,t.jsx)(n.p,{children:(0,t.jsx)(n.img,{alt:"Badger architecture",src:i(4224).Z+"",width:"1797",height:"844"})}),"\n",(0,t.jsx)(n.p,{children:"Badger abstracts an optimization run as an optimization algorithm interacts with an environment, by following some pre-defined rules. As visualized in the picture above, the environment is controlled by the algorithm and tunes/observes the control system/machine through an interface, while the users control/monitor the optimization flow through a graphical user interface (GUI) or a command line interface (CLI)."}),"\n",(0,t.jsx)(n.p,{children:"Algorithms, environments, and interfaces in Badger are all managed through a plugin system, and could be developed and maintained separately. The application interfaces (API) for creating the plugins are very straightforward and simple, yet abstractive enough to handle various situations."}),"\n",(0,t.jsx)(n.p,{children:"Badger offers 3 modes to satisfy different user groups:"}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:"GUI mode, for ACR operators, enable them to perform regular optimization tasks with one click"}),"\n",(0,t.jsx)(n.li,{children:"CLI mode, for the command line lovers or the situation without a screen, configure and run the whole optimization in one line efficiently"}),"\n",(0,t.jsx)(n.li,{children:"API mode, for the algorithm developers, use the environments provided by Badger without the troubles to configure them"}),"\n"]}),"\n",(0,t.jsx)(n.h2,{id:"important-concepts",children:"Important concepts"}),"\n",(0,t.jsx)(n.p,{children:"As shown in the Badger schematic plot above, there are several terms/concepts in Badger, and their meaning are a little different with regard to their general definitions. Let's briefly go through the terms/concepts in Badger in the following sections."}),"\n",(0,t.jsx)(n.h3,{id:"routine",children:"Routine"}),"\n",(0,t.jsx)(n.p,{children:"An optimization setup in Badger is called a routine. A routine contains all the information needed to perform the optimization:"}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:"The optimization algorithm and its hyperparameters"}),"\n",(0,t.jsx)(n.li,{children:"The environment on which the optimization would be performed"}),"\n",(0,t.jsx)(n.li,{children:"The configuration of the optimization, such as variables, objectives, and constraints"}),"\n"]}),"\n",(0,t.jsx)(n.p,{children:"To run an optimization in Badger, the users need to define the routine. Badger provides several ways to easily compose the routine, so no worries, you'll not have to write it by hands:)"}),"\n",(0,t.jsx)(n.h3,{id:"interface",children:"Interface"}),"\n",(0,t.jsx)(n.p,{children:"An interface in Badger is a piece of code that talks to the underlying control system/machine. It communicates to the control system to:"}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:"Set a process variable (PV) to some specific value"}),"\n",(0,t.jsx)(n.li,{children:"Get the value of a PV"}),"\n"]}),"\n",(0,t.jsxs)(n.p,{children:["An interface is also responsible to perform the configuration needed for communicating with the control system, and the configuration can be customized by passing a ",(0,t.jsx)(n.code,{children:"params"})," dictionary to the interface."]}),"\n",(0,t.jsx)(n.p,{children:"The concept of interface was introduced to Badger for better code reuse. You don't have to copy-n-paste the same fundamental code again and again when coding your optimization problems for the same underlying control system. Now you could simply ask Badger to use the same interface, and focus more on the higher level logic of the problem."}),"\n",(0,t.jsx)(n.admonition,{type:"tip",children:(0,t.jsxs)(n.p,{children:["Interfaces are ",(0,t.jsx)(n.strong,{children:"optional"})," in Badger -- an interface is not needed if the optimization problem is simple enough (say, analytical function) that you can directly shape it into an environment."]})}),"\n",(0,t.jsx)(n.h3,{id:"environment",children:"Environment"}),"\n",(0,t.jsxs)(n.p,{children:["An environment is Badger's way to (partially) abstract an optimization problem. A typical optimization problem usually consists of the variables to tune, and the objectives to optimize. A Badger environment defines all the interested ",(0,t.jsx)(n.strong,{children:"variables"})," and ",(0,t.jsx)(n.strong,{children:"observations"})," of a control system/machine. An optimization problem can be specified by stating which variables in the environment are the variables to tune, and which observations are the objectives to optimize. Furthermore, one can define the constraints for the optimization by picking up some observation from the environment and giving it a threshold."]}),"\n",(0,t.jsxs)(n.p,{children:["Take the following case as an example. Assume that we have an accelerator control system and we'd like to tune the quadupoles ",(0,t.jsx)(n.code,{children:"QUAD:1"}),", ",(0,t.jsx)(n.code,{children:"QUAD:2"})," and minimize the horizontal beam size on a screen ",(0,t.jsx)(n.code,{children:"BSIZE:X"}),". We also want to keep the vertical beam size ",(0,t.jsx)(n.code,{children:"BSIZE:Y"})," below a certain value. To do this in Badger, we could define an environment that has variables:"]}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:(0,t.jsx)(n.code,{children:"QUAD:1"})}),"\n",(0,t.jsx)(n.li,{children:(0,t.jsx)(n.code,{children:"QUAD:2"})}),"\n"]}),"\n",(0,t.jsx)(n.p,{children:"And observations:"}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:(0,t.jsx)(n.code,{children:"BSIZE:X"})}),"\n",(0,t.jsx)(n.li,{children:(0,t.jsx)(n.code,{children:"BSIZE:Y"})}),"\n"]}),"\n",(0,t.jsxs)(n.p,{children:["Then define a ",(0,t.jsx)(n.strong,{children:(0,t.jsx)(n.a,{href:"#routine-config",children:"routine config"})})," to specify details of the optimization problem, as will be mentioned in the next section."]}),"\n",(0,t.jsx)(n.admonition,{type:"tip",children:(0,t.jsxs)(n.p,{children:["One environment could support multiple ",(0,t.jsx)(n.strong,{children:"relevant"})," optimization problems -- just put all the variables and observations to the environment, and use routine config to select which variables/observations to use for the optimization."]})}),"\n",(0,t.jsx)(n.h3,{id:"routine-config",children:"Routine config"}),"\n",(0,t.jsx)(n.p,{children:"A routine config is the counterpart of optimization problem abstraction with regard to environment. An optimization problem can be fully defined by an environment with a routine config."}),"\n",(0,t.jsx)(n.p,{children:"On top of the variables and observations provided by environment, routine config tells Badger which and how variables/observations are used as the tuning variables/objectives/constraints."}),"\n",(0,t.jsx)(n.p,{children:"Use the example from the last section, the routine config for the problem could be:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-yaml",metastring:'title="Routine Config"',children:"variables:\n  - QUAD:1\n  - QUAD:2\nobjectives:\n  - BSIZE:X: MINIMIZE\nconstraints:\n  - BSIZE:Y:\n      - LESS_THAN\n      - 0.5\n"})}),"\n",(0,t.jsx)(n.p,{children:"The reasons to divide the optimization problem definition into two parts (environment and routine config) are:"}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:"Better code reuse"}),"\n",(0,t.jsx)(n.li,{children:"Operations in ACR usually require slightly changing a routine frequently, so it's good to have an abstraction for the frequently changed configurations (routine config), to avoid messing with the optimization source code"}),"\n"]}),"\n",(0,t.jsx)(n.h2,{id:"features",children:"Features"}),"\n",(0,t.jsx)(n.p,{children:"One of Badger's core features is the ability to extend easily. Badger offers two ways to extend its capibility: making a plugin, or implementing an extension."}),"\n",(0,t.jsx)(n.h3,{id:"plugin-system",children:"Plugin system"}),"\n",(0,t.jsx)(n.p,{children:"Algorithms, interfaces, and environments are all plugins in Badger. A plugin in Badger is a set of python scripts, a YAML config file, and an optional README.md. A typical file structure of a plugin looks like:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-shell",metastring:'title="Plugin File Structure"',children:"|--<PLUGIN_ID>\n    |--__init__.py\n    |--configs.yaml\n    |--README.md\n    |--...\n"})}),"\n",(0,t.jsxs)(n.p,{children:["The role/feature of each file will be discussed in details later in the ",(0,t.jsx)(n.a,{href:"guides/create-a-plugin",children:"create a plugin"})," section."]}),"\n",(0,t.jsx)(n.admonition,{type:"tip",children:(0,t.jsx)(n.p,{children:"One unique feature of Badger plugins is that plugins can be nested -- you can use any available plugins inside your own plugin. Say, one could combine two environments and create a new one effortlessly, thanks to this nestable nature of Badger plugins. You could explore the infinity possibilities by nesting plugins together with your imagination!"})}),"\n",(0,t.jsx)(n.h3,{id:"extension-system",children:"Extension system"}),"\n",(0,t.jsx)(n.p,{children:"Extension system is another way to extend Badger's capabilities, and in a sense it's more powerful than the plugin system, since it could make a batch of existing algorithms available in Badger in a few lines of code!"}),"\n",(0,t.jsxs)(n.p,{children:["Let's assume that we already have an optimization platform/framework that provides a dozen of algorithms, and we'd like to use these algorithms to optimize on our machine environment. One way to do that is porting all these algorthms to Badger through the plugin system, and use Badger to perform the optimization. Extension system was designed just for this situation, since porting the algorithms one by one is tedious and inefficient. Extension system provides the APIs that are required to be implemented in order to \"port\" all the algorithms of another optimization framework/platform in one go. More details about extension system can be found in the ",(0,t.jsx)(n.a,{href:"guides/implement-an-extension",children:"implement an extension"})," section."]}),"\n",(0,t.jsx)(n.p,{children:"With the extension system, Badger could use any existing algorithms from another optimization package. Currently, Badger has the following extensions available:"}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:(0,t.jsx)(n.a,{href:"https://github.com/ChristopherMayes/Xopt",children:"xopt"})}),"\n"]}),"\n",(0,t.jsxs)(n.p,{children:["And more extensions are on the way (for example, ",(0,t.jsx)(n.a,{href:"https://teeport.ml/intro",children:"teeport"})," extension for remote optimization)!"]})]})}function h(e={}){const{wrapper:n}={...(0,o.a)(),...e.components};return n?(0,t.jsx)(n,{...e,children:(0,t.jsx)(d,{...e})}):d(e)}},4224:(e,n,i)=>{i.d(n,{Z:()=>t});const t=i.p+"assets/images/architecture-b0910240b36cb72a945230d415864f3a.png"},1151:(e,n,i)=>{i.d(n,{Z:()=>a,a:()=>s});var t=i(7294);const o={},r=t.createContext(o);function s(e){const n=t.useContext(r);return t.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function a(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(o):e.components||o:s(e.components),t.createElement(r.Provider,{value:n},e.children)}}}]);