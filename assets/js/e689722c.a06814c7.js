"use strict";(self.webpackChunkbadger_home=self.webpackChunkbadger_home||[]).push([[276],{9535:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>l,contentTitle:()=>r,default:()=>u,frontMatter:()=>s,metadata:()=>o,toc:()=>c});var a=t(5893),i=t(1151);const s={sidebar_position:1},r="API Usage",o={id:"guides/api-usage",title:"API Usage",description:"Badger can be imported as a regular python package, and you could use the plugins/utils that Badger offers in your own python script.",source:"@site/docs/guides/api-usage.md",sourceDirName:"guides",slug:"/guides/api-usage",permalink:"/Badger/docs/guides/api-usage",draft:!1,unlisted:!1,editUrl:"https://github.com/SLAC-ML/Badger-Home/edit/master/docs/guides/api-usage.md",tags:[],version:"current",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"tutorialSidebar",previous:{title:"Tutorial",permalink:"/Badger/docs/getting-started/tutorial"},next:{title:"CLI Usage",permalink:"/Badger/docs/guides/cli-usage"}},l={},c=[{value:"Use an algorithm",id:"use-an-algorithm",level:2},{value:"Use an interface",id:"use-an-interface",level:2},{value:"Use an environment",id:"use-an-environment",level:2}];function d(e){const n={a:"a",admonition:"admonition",code:"code",h1:"h1",h2:"h2",p:"p",pre:"pre",...(0,i.a)(),...e.components};return(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(n.h1,{id:"api-usage",children:"API Usage"}),"\n",(0,a.jsx)(n.p,{children:"Badger can be imported as a regular python package, and you could use the plugins/utils that Badger offers in your own python script."}),"\n",(0,a.jsx)(n.admonition,{title:"Heads-up",type:"note",children:(0,a.jsxs)(n.p,{children:["Make sure you have Badger ",(0,a.jsx)(n.a,{href:"../getting-started/installation",children:"installed and setup"}),"."]})}),"\n",(0,a.jsx)(n.h2,{id:"use-an-algorithm",children:"Use an algorithm"}),"\n",(0,a.jsxs)(n.p,{children:["Badger has a ",(0,a.jsx)(n.code,{children:"get_algo"})," API to get a specific algorithm."]}),"\n",(0,a.jsxs)(n.p,{children:["The following code gets an algorithm named ",(0,a.jsx)(n.code,{children:"silly"})," (which is a random search algorithm) from Badger."]}),"\n",(0,a.jsx)(n.pre,{children:(0,a.jsx)(n.code,{className:"language-python",children:"import numpy as np\nfrom badger.factory import get_algo\n\n# Define a test evaluate function\ndef evaluate(X):\n    Y = np.linalg.norm(X, axis=1).reshape(-1, 1)  # objectives\n    I = None  # inequality constraints\n    E = None  # equality constraints\n\n    # Show the progress\n    print(Y)\n\n    return Y, I, E\n\n# Get the silly algorithm from Badger\noptimize, configs = get_algo('silly')\n\n# Optimize the test evaluate function\noptimize(evaluate, configs['params'])\n"})}),"\n",(0,a.jsx)(n.h2,{id:"use-an-interface",children:"Use an interface"}),"\n",(0,a.jsxs)(n.p,{children:["Badger has a ",(0,a.jsx)(n.code,{children:"get_intf"})," API to get a specific interface."]}),"\n",(0,a.jsxs)(n.p,{children:["The following code gets an interface named ",(0,a.jsx)(n.code,{children:"silly"})," and constructs an instance of the interface."]}),"\n",(0,a.jsx)(n.pre,{children:(0,a.jsx)(n.code,{className:"language-python",children:"from badger.factory import get_intf\n\n# Get the silly interface from Badger\nInterface, configs = get_intf('silly')\nintf = Interface(configs['params'])\n\n# Test get/set channels\nintf.get_value('c1')\n# Output: 0\n\nintf.set_value('c1', 1.0)\nintf.get_value('c1')\n# Output: 1.0\n"})}),"\n",(0,a.jsx)(n.h2,{id:"use-an-environment",children:"Use an environment"}),"\n",(0,a.jsxs)(n.p,{children:["Badger has a ",(0,a.jsx)(n.code,{children:"get_env"})," API to get a specific environment."]}),"\n",(0,a.jsxs)(n.p,{children:["The following code gets and instantiates an environment named ",(0,a.jsx)(n.code,{children:"silly"})," from Badger. Note that it uses the ",(0,a.jsx)(n.code,{children:"silly"})," interface instance ",(0,a.jsx)(n.code,{children:"intf"})," from the ",(0,a.jsx)(n.a,{href:"#use-an-interface",children:"last"})," section."]}),"\n",(0,a.jsx)(n.pre,{children:(0,a.jsx)(n.code,{className:"language-python",children:"from badger.factory import get_env\n\n# Get the silly environment from Badger\nEnvironment, configs = get_env('silly')\nenv = Environment(intf, configs['params'])\n\n# Investigate the silly env\nenv.list_vars()\n# Output: ['q1', 'q2', 'q3', 'q4']\n\nenv.list_obses()\n# Output: ['l1', 'l2']\n\nenv.get_var('q1')  # q1 in env maps to c1 in intf\n# Output: 1.0\n\nenv.get_obs('l2')  # l2 norm of (q1, q2, q3, q4)\n# Output: 1.0\n\nenv.set_var('q2', 1)\nenv.get_obs('l2')\n# Output: 1.4142135623730951\n"})}),"\n",(0,a.jsxs)(n.p,{children:["Now we can define an evaluate function based on the ",(0,a.jsx)(n.code,{children:"silly"})," env, and use the ",(0,a.jsx)(n.code,{children:"silly"})," algorithm from the ",(0,a.jsx)(n.a,{href:"#use-an-algorithm",children:"use an algorithm"})," section to optimize it."]}),"\n",(0,a.jsx)(n.pre,{children:(0,a.jsx)(n.code,{className:"language-python",children:"# Define an evaluate function based on the env\ndef evaluate(X):\n    # Note that X is a 2D array\n    Y = []\n    for x in X:\n        env.set_vars(['q1', 'q2', 'q3', 'q4'][:len(x)], x)\n        y = env.get_obs('l2')\n        Y.append(y)\n    Y = np.array(Y).reshape(-1, 1)\n    I = None\n    E = None\n\n    # Show the progress\n    print(Y)\n\n    return Y, I, E\n\n# Optimize the evaluate function with silly algorithm\noptimize(evaluate, {'dimension': 4, 'max_iter': 42})\n"})})]})}function u(e={}){const{wrapper:n}={...(0,i.a)(),...e.components};return n?(0,a.jsx)(n,{...e,children:(0,a.jsx)(d,{...e})}):d(e)}},1151:(e,n,t)=>{t.d(n,{Z:()=>o,a:()=>r});var a=t(7294);const i={},s=a.createContext(i);function r(e){const n=a.useContext(s);return a.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function o(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(i):e.components||i:r(e.components),a.createElement(s.Provider,{value:n},e.children)}}}]);