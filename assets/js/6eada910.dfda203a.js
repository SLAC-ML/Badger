"use strict";(self.webpackChunkbadger_home=self.webpackChunkbadger_home||[]).push([[769],{381:(n,e,t)=>{t.r(e),t.d(e,{assets:()=>l,contentTitle:()=>r,default:()=>h,frontMatter:()=>o,metadata:()=>s,toc:()=>d});var i=t(5893),a=t(1151);const o={sidebar_position:2},r="Tutorial",s={id:"getting-started/tutorial",title:"Tutorial",description:"Make sure you have Badger installed and setup.",source:"@site/docs/getting-started/tutorial.md",sourceDirName:"getting-started",slug:"/getting-started/tutorial",permalink:"/Badger/docs/next/getting-started/tutorial",draft:!1,unlisted:!1,editUrl:"https://github.com/SLAC-ML/Badger-Home/edit/master/docs/getting-started/tutorial.md",tags:[],version:"current",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"Installation",permalink:"/Badger/docs/next/getting-started/installation"},next:{title:"API Usage",permalink:"/Badger/docs/next/guides/api-usage"}},l={},d=[{value:"Get basic information about Badger",id:"get-basic-information-about-badger",level:2},{value:"Run and save an optimization",id:"run-and-save-an-optimization",level:2},{value:"Rerun an optimization",id:"rerun-an-optimization",level:2},{value:"View the historical optimization data",id:"view-the-historical-optimization-data",level:2},{value:"Create a simple environment",id:"create-a-simple-environment",level:2}];function c(n){const e={a:"a",admonition:"admonition",code:"code",h1:"h1",h2:"h2",p:"p",pre:"pre",strong:"strong",...(0,a.a)(),...n.components};return(0,i.jsxs)(i.Fragment,{children:[(0,i.jsx)(e.h1,{id:"tutorial",children:"Tutorial"}),"\n",(0,i.jsx)(e.admonition,{title:"Heads-up",type:"note",children:(0,i.jsxs)(e.p,{children:["Make sure you have Badger ",(0,i.jsx)(e.a,{href:"./installation",children:"installed and setup"}),"."]})}),"\n",(0,i.jsxs)(e.p,{children:["Let's discover ",(0,i.jsx)(e.strong,{children:"Badger in less than 5 minutes"}),". All of the following commands are assumed to be run in a terminal (Mac, Windows, and Linux are supported)."]}),"\n",(0,i.jsx)(e.h2,{id:"get-basic-information-about-badger",children:"Get basic information about Badger"}),"\n",(0,i.jsx)(e.p,{children:"First let's verify that Badger has been installed and configured correctly:"}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-shell",children:"badger\n"})}),"\n",(0,i.jsx)(e.p,{children:"Which should give you something like:"}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-shell",metastring:'title="output"',children:"name: Badger the optimizer\nversion: 0.5.3\nplugin root: /root/badger/plugins\ndatabase root: /root/badger/db\nlogbook root: /root/badger/logbook\narchive root: /root/badger/archived\nextensions:\n  - xopt\n"})}),"\n",(0,i.jsx)(e.h2,{id:"run-and-save-an-optimization",children:"Run and save an optimization"}),"\n",(0,i.jsxs)(e.p,{children:["Create a yaml file under your ",(0,i.jsx)(e.code,{children:"pwd"})," (where you would run an optimization with Badger) with the following content:"]}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-yaml",metastring:'title="config.yaml"',children:"variables:\n  - x2\nobjectives:\n  - c1\n"})}),"\n",(0,i.jsx)(e.p,{children:"To run and save an optimization, run:"}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-shell",children:"badger run -a silly -e TNK -c config.yaml -s helloworld\n"})}),"\n",(0,i.jsx)(e.p,{children:"Badger will ask you to review the optimization routine:"}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-shell",metastring:'title="output"',children:"Please review the routine to be run:\n\n=== Optimization Routine ===\nname: mottled-sloth\nalgo: silly\nenv: TNK\nalgo_params:\n  dimension: 1\n  max_iter: 42\nenv_params: null\nconfig:\n  variables:\n    - x2: 0 -> 3.14159\n  objectives:\n    - c1: MINIMIZE\n  constraints: null\n\nProceed ([y]/n)?\n"})}),"\n",(0,i.jsx)(e.p,{children:"Hit return to confirm. Badger will print out a table of all the evaluated\nsolutions along the run:"}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-shell",metastring:'{3,19} title="output"',children:"|    iter    |     c1     |     x2     |\n----------------------------------------\n|  1         | -1.094     |  0.07432   |\n|  2         |  3.563     |  2.159     |\n|  3         |  8.749     |  3.138     |\n|  4         |  5.351     |  2.54      |\n|  5         |  8.17      |  3.045     |\n|  6         |  6.536     |  2.763     |\n|  7         |  3.007     |  2.027     |\n|  8         | -1.089     |  0.1063    |\n|  9         |  4.127     |  2.286     |\n|  10        |  3.519     |  2.149     |\n|  11        |  6.647     |  2.783     |\n|  12        |  1.074     |  1.474     |\n|  13        | -0.8621    |  0.4878    |\n|  14        |  3.821     |  2.218     |\n|  15        | -0.9228    |  0.421     |\n|  16        |  6.205     |  2.703     |\n|  17        | -1.1       |  0.005409  |\n|  18        |  8.224     |  3.054     |\n|  19        |  7.584     |  2.947     |\n|  20        | -0.8961    |  0.4515    |\n|  21        | -1.093     |  0.08082   |\n|  22        |  1.293     |  1.547     |\n|  23        |  2.593     |  1.922     |\n|  24        |  5.563     |  2.581     |\n|  25        |  2.046     |  1.774     |\n|  26        |  2.501     |  1.898     |\n|  27        | -0.8853    |  0.4633    |\n|  28        | -0.5459    |  0.7444    |\n|  29        | -0.8881    |  0.4604    |\n|  30        | -0.4806    |  0.787     |\n|  31        | -1.1       |  0.01909   |\n|  32        |  0.4855    |  1.259     |\n|  33        |  0.8217    |  1.386     |\n|  34        |  6.036     |  2.671     |\n|  35        | -0.7649    |  0.5789    |\n|  36        |  0.06972   |  1.082     |\n|  37        |  7.325     |  2.903     |\n|  38        | -0.7764    |  0.5689    |\n|  39        |  6.042     |  2.673     |\n|  40        |  5.008     |  2.471     |\n|  41        |  4.274     |  2.318     |\n|  42        | -0.8561    |  0.4939    |\n========================================\n"})}),"\n",(0,i.jsxs)(e.p,{children:["You would notice that the optimal solutions (in this case\noptimal means minimal ",(0,i.jsx)(e.code,{children:"c1"}),") at the evaluation time are highlighted."]}),"\n",(0,i.jsxs)(e.p,{children:["In the example above, we use the ",(0,i.jsx)(e.strong,{children:"silly"})," algorithm (which is just a random search algorithm) to optimize the ",(0,i.jsx)(e.strong,{children:"TNK"}),"\nenvironment, as shown in the reviewed routine. Environment ",(0,i.jsx)(e.strong,{children:"TNK"})," has 2\nvariables and 5 observations:"]}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-yaml",metastring:'{7,8,10-14} title="TNK environment"',children:"name: TNK\nversion: '0.1'\ndependencies:\n  - numpy\nparams: null\nvariables:\n  - x1: 0 -> 3.14159\n  - x2: 0 -> 3.14159\nobservations:\n  - y1\n  - y2\n  - c1\n  - c2\n  - some_array\n"})}),"\n",(0,i.jsxs)(e.p,{children:["We specify in the ",(0,i.jsx)(e.code,{children:"config.yaml"})," that we would like to tune varaible ",(0,i.jsx)(e.code,{children:"x2"}),", and minimize observation ",(0,i.jsx)(e.code,{children:"c1"})," of environment ",(0,i.jsx)(e.strong,{children:"TNK"})," as objective. The configuration that could reproduce the whole optimization setup is called a ",(0,i.jsx)(e.strong,{children:"routine"})," in Badger. A routine contains the information of the algorithm, the environment, and the config of the optimization (the variables, the objectives, and the constraints)."]}),"\n",(0,i.jsxs)(e.p,{children:["We just saved the routine of the run as ",(0,i.jsx)(e.code,{children:"helloworld"}),". Now you could view the routine again by:"]}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-shell",children:"badger routine helloworld\n"})}),"\n",(0,i.jsx)(e.h2,{id:"rerun-an-optimization",children:"Rerun an optimization"}),"\n",(0,i.jsxs)(e.p,{children:["We can rerun a saved routine in Badger. Let's rerun the ",(0,i.jsx)(e.code,{children:"helloworld"})," routine that we just saved:"]}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-shell",children:"badger routine helloworld -r\n"})}),"\n",(0,i.jsx)(e.p,{children:"Badger would behave exactly the same way as the first time you run the routine."}),"\n",(0,i.jsx)(e.h2,{id:"view-the-historical-optimization-data",children:"View the historical optimization data"}),"\n",(0,i.jsxs)(e.p,{children:["You can ",(0,i.jsx)(e.code,{children:"cd"})," to the Badger archive root (the one you setup during the initial configurations) and view the historical optimization data. The file structure is a tree-like one, with year, year-month, year-month-day as the first 3 levels of branches, and the optimization runs as leaves:"]}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-shell",metastring:'{4} title="Badger archive root file structure"',children:"|--2021\n    |--2021-11\n        |--2021-11-24\n            |--BadgerOpt-2021-11-24-133007.yaml\n            |--BadgerOpt-2021-11-24-113241.yaml\n            |--...\n        |--...\n    |--...\n|--...\n"})}),"\n",(0,i.jsx)(e.p,{children:"The yaml data file contains the routine information and the solutions evaluated during the run. The content would look like this:"}),"\n",(0,i.jsx)(e.pre,{children:(0,i.jsx)(e.code,{className:"language-yaml",metastring:'title="BadgerOpt-2021-11-24-133007.yaml"',children:"routine:\n  name: helloworld\n  algo: silly\n  env: TNK\n  algo_params:\n    dimension: 1\n    max_iter: 10\n  env_params: null\n  config:\n    variables:\n      - x2:\n          - 0.0\n          - 3.1416\n    objectives:\n      - c1: MINIMIZE\n    constraints: null\ndata:\n  timestamp:\n    - 24-Nov-2021 13:30:06\n    - 24-Nov-2021 13:30:06\n    - 24-Nov-2021 13:30:06\n    - 24-Nov-2021 13:30:06\n    - 24-Nov-2021 13:30:06\n    - 24-Nov-2021 13:30:06\n    - 24-Nov-2021 13:30:06\n    - 24-Nov-2021 13:30:07\n    - 24-Nov-2021 13:30:07\n    - 24-Nov-2021 13:30:07\n  c1:\n    - 2.093905436806936\n    - 2.6185501712620036\n    - -0.8170601778601619\n    - 7.869183841178197\n    - -1.0945113202011\n    - 0.514833333947652\n    - -1.0331173238615994\n    - 1.4523371516674013\n    - 1.3610274948700156\n    - -0.0042273815683477045\n  x2:\n    - 1.78715008793524\n    - 1.9283542649788197\n    - 0.5319208795862764\n    - 2.9948595695254556\n    - 0.07408562477903413\n    - 1.2707609271407632\n    - 0.2586168520000207\n    - 1.5976035652399507\n    - 1.5687662333407153\n    - 1.0467915830917118\n"})}),"\n",(0,i.jsx)(e.h2,{id:"create-a-simple-environment",children:"Create a simple environment"}),"\n",(0,i.jsx)(e.p,{children:"Now let's create a simple Badger environment and run optimization on it."}),"\n",(0,i.jsx)(e.p,{children:(0,i.jsx)(e.strong,{children:"WIP"})})]})}function h(n={}){const{wrapper:e}={...(0,a.a)(),...n.components};return e?(0,i.jsx)(e,{...n,children:(0,i.jsx)(c,{...n})}):c(n)}},1151:(n,e,t)=>{t.d(e,{Z:()=>s,a:()=>r});var i=t(7294);const a={},o=i.createContext(a);function r(n){const e=i.useContext(o);return i.useMemo((function(){return"function"==typeof n?n(e):{...e,...n}}),[e,n])}function s(n){let e;return e=n.disableParentContext?"function"==typeof n.components?n.components(a):n.components||a:r(n.components),i.createElement(o.Provider,{value:e},n.children)}}}]);