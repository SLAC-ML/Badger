"use strict";(self.webpackChunkbadger_home=self.webpackChunkbadger_home||[]).push([[2868],{6650:(e,n,i)=>{i.r(n),i.d(n,{assets:()=>t,contentTitle:()=>l,default:()=>h,frontMatter:()=>r,metadata:()=>o,toc:()=>d});var s=i(5893),a=i(1151);const r={sidebar_position:2},l="CLI Usage",o={id:"guides/cli-usage",title:"CLI Usage",description:"For all the implemented and planned CLI usage, please refer to these slides. We'll highlight several common CLI use cases of Badger in the following sections.",source:"@site/versioned_docs/version-0.11/guides/cli-usage.md",sourceDirName:"guides",slug:"/guides/cli-usage",permalink:"/Badger/docs/guides/cli-usage",draft:!1,unlisted:!1,editUrl:"https://github.com/SLAC-ML/Badger-Home/edit/master/versioned_docs/version-0.11/guides/cli-usage.md",tags:[],version:"0.11",sidebarPosition:2,frontMatter:{sidebar_position:2},sidebar:"tutorialSidebar",previous:{title:"API Usage",permalink:"/Badger/docs/guides/api-usage"},next:{title:"GUI Usage",permalink:"/Badger/docs/guides/gui-usage"}},t={},d=[{value:"Get help",id:"get-help",level:2},{value:"Show metadata of Badger",id:"show-metadata-of-badger",level:2},{value:"Get information of the algorithms",id:"get-information-of-the-algorithms",level:2},{value:"Get information of the environments",id:"get-information-of-the-environments",level:2},{value:"Run and save an optimization",id:"run-and-save-an-optimization",level:2},{value:"A simplest run command",id:"a-simplest-run-command",level:3},{value:"Run without confirmation",id:"run-without-confirmation",level:3},{value:"Change verbose level",id:"change-verbose-level",level:3},{value:"Configure algorithm/environment parameters",id:"configure-algorithmenvironment-parameters",level:3},{value:"Run with algorithms provided by extensions",id:"run-with-algorithms-provided-by-extensions",level:3},{value:"Save a run",id:"save-a-run",level:3},{value:"Rerun a saved optimization routine",id:"rerun-a-saved-optimization-routine",level:2},{value:"Configure Badger",id:"configure-badger",level:2},{value:"Launch the Badger GUI",id:"launch-the-badger-gui",level:2}];function c(e){const n={a:"a",code:"code",h1:"h1",h2:"h2",h3:"h3",li:"li",p:"p",pre:"pre",ul:"ul",...(0,a.a)(),...e.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(n.h1,{id:"cli-usage",children:"CLI Usage"}),"\n",(0,s.jsxs)(n.p,{children:["For all the implemented and planned CLI usage, please refer to ",(0,s.jsx)(n.a,{href:"https://docs.google.com/presentation/d/1APlLgaRik2VPGL7FuxEUmwHvx6egTeIRaxBKGS1TnsE/edit#slide=id.ge68b2a5657_0_5",children:"these slides"}),". We'll highlight several common CLI use cases of Badger in the following sections."]}),"\n",(0,s.jsx)(n.h2,{id:"get-help",children:"Get help"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger -h\n"})}),"\n",(0,s.jsxs)(n.p,{children:["Or ",(0,s.jsx)(n.a,{href:"mailto:zhezhang@slac.stanford.edu",children:"shoot me an email"}),"!"]}),"\n",(0,s.jsx)(n.h2,{id:"show-metadata-of-badger",children:"Show metadata of Badger"}),"\n",(0,s.jsx)(n.p,{children:"To show the version number and some other metadata such as plugin directory:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger\n"})}),"\n",(0,s.jsx)(n.h2,{id:"get-information-of-the-algorithms",children:"Get information of the algorithms"}),"\n",(0,s.jsx)(n.p,{children:"List all the available algorithms:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger algo\n"})}),"\n",(0,s.jsx)(n.p,{children:"Get the configs of a specific algorithm:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger algo ALGO_NAME\n"})}),"\n",(0,s.jsx)(n.p,{children:"You'll get something like:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-yaml",children:"name: silly\nversion: '0.1'\ndependencies:\n  - numpy\nparams:\n  dimension: 1\n  max_iter: 42\n"})}),"\n",(0,s.jsxs)(n.p,{children:["Note that in order to use this plugin, you'll need to install the dependencies listed in the command output. This dependency installation will be handled automatically if the plugin was installed through the ",(0,s.jsx)(n.code,{children:"badger install"})," command, but that command is not available yet (it is coming soon)."]}),"\n",(0,s.jsxs)(n.p,{children:["The ",(0,s.jsx)(n.code,{children:"params"})," part shows all the intrinsic parameters that can be tuned when doing optimization with this algorithm."]}),"\n",(0,s.jsx)(n.h2,{id:"get-information-of-the-environments",children:"Get information of the environments"}),"\n",(0,s.jsx)(n.p,{children:"List all the available environments:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger env\n"})}),"\n",(0,s.jsx)(n.p,{children:"Get the configs of a specific environment:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger env ENV_NAME\n"})}),"\n",(0,s.jsx)(n.p,{children:"The command will print out something like:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-yaml",children:"name: dumb\nversion: '0.1'\ndependencies:\n  - numpy\n  - badger-opt\ninterface:\n  - silly\nenvironments:\n  - silly\n  - naive\nparams: null\nvariables:\n  - q1: 0 -> 1\n  - q2: 0 -> 1\n  - q3: 0 -> 1\n  - q4: 0 -> 1\n  - s1: 0 -> 1\n  - s2: 0 -> 1\nobservations:\n  - l2\n  - mean\n  - l2_x_mean\n"})}),"\n",(0,s.jsx)(n.p,{children:"There are several important properties here:"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.code,{children:"variables"}),": The tunable variables provided by this environment. You could choose a subset of the variables as the desicion variables for the optimization in the routine config. The allowed ranges (in this case, 0 to 1) are shown behind the corresponding variable names"]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.code,{children:"observations"}),": The measurements provided by this environment. You could choose some observations as the objectives, and some other observations as the constraints in the routine config"]}),"\n"]}),"\n",(0,s.jsx)(n.h2,{id:"run-and-save-an-optimization",children:"Run and save an optimization"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger run [-h] -a ALGO_NAME [-ap ALGO_PARAMS] -e ENV_NAME [-ep ENV_PARAMS] -c ROUTINE_CONFIG [-s [SAVE_NAME]] [-y] [-v [{0,1,2}]]\n"})}),"\n",(0,s.jsxs)(n.p,{children:["The ",(0,s.jsx)(n.code,{children:"-ap"})," and ",(0,s.jsx)(n.code,{children:"-ep"})," optional arguments, and the ",(0,s.jsx)(n.code,{children:"-c"})," argument accept either a ",(0,s.jsx)(n.code,{children:".yaml"})," file path or a yaml string. The configs set to ",(0,s.jsx)(n.code,{children:"-ap"})," and ",(0,s.jsx)(n.code,{children:"-ep"}),' optional arguments should be treated as "patch" on the default algorithm and environment parameters, respectively, which means that you only need to specify the paramters that you\'d like to change on top of the default configs, rather than pass in a full config. The content of the ',(0,s.jsx)(n.code,{children:"ROUTINE_CONFIG"})," (aka routine configs) should look like this:"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-yaml",children:"variables:\n  - x1: [-1, 0.5]\n  - x2\nobjectives:\n  - c1\n  - y2: MINIMIZE\nconstraints:\n  - y1:\n      - GREATER_THAN\n      - 0\n  - c2:\n      - LESS_THAN\n      - 0.5\n"})}),"\n",(0,s.jsxs)(n.p,{children:["The ",(0,s.jsx)(n.code,{children:"variables"})," and ",(0,s.jsx)(n.code,{children:"objectives"})," properties are required, while the ",(0,s.jsx)(n.code,{children:"constraints"})," property is optional. Just omit the ",(0,s.jsx)(n.code,{children:"constraints"})," property if there are no constraints for your optimization problem. The names listed in ",(0,s.jsx)(n.code,{children:"variables"})," should come from ",(0,s.jsx)(n.code,{children:"variables"})," of the env specified by the ",(0,s.jsx)(n.code,{children:"-e"})," argument, while the names listed in ",(0,s.jsx)(n.code,{children:"objectives"})," and ",(0,s.jsx)(n.code,{children:"constraints"})," should come from ",(0,s.jsx)(n.code,{children:"observations"})," of that env."]}),"\n",(0,s.jsxs)(n.p,{children:["All optimization runs will be archived in the ",(0,s.jsx)(n.code,{children:"$BADGER_ARCHIVE_ROOT"})," folder that you initially set up when running ",(0,s.jsx)(n.code,{children:"badger"})," the first time."]}),"\n",(0,s.jsxs)(n.p,{children:["Several example routine configs can be found in the ",(0,s.jsx)(n.code,{children:"examples"})," folder."]}),"\n",(0,s.jsxs)(n.p,{children:["Below are some example ",(0,s.jsx)(n.code,{children:"badger run"})," commands. They are assumed to run under the parent directory of the ",(0,s.jsx)(n.code,{children:"examples"})," folder (you'll need to clone the ",(0,s.jsx)(n.code,{children:"examples"})," folder from this repo to your computer first). You could run them from any directory, just remember to change the routine config path accordingly."]}),"\n",(0,s.jsx)(n.h3,{id:"a-simplest-run-command",children:"A simplest run command"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger run -a silly -e TNK -c examples/silly_tnk.yaml\n"})}),"\n",(0,s.jsx)(n.h3,{id:"run-without-confirmation",children:"Run without confirmation"}),"\n",(0,s.jsxs)(n.p,{children:["Badger will let you confirm the routine before running it. You could skip the confirmation by adding the ",(0,s.jsx)(n.code,{children:"-y"})," option:"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger run -a silly -e TNK -c examples/silly_tnk.yaml -y\n"})}),"\n",(0,s.jsx)(n.h3,{id:"change-verbose-level",children:"Change verbose level"}),"\n",(0,s.jsxs)(n.p,{children:["By default, Badger will print out a table contains all the evaluated solutions along the optimization run (with the optimal ones highlighted), you could alter the default behavior by setting the ",(0,s.jsx)(n.code,{children:"-v"})," option."]}),"\n",(0,s.jsx)(n.p,{children:"The default verbose level 2 will print out all the solutions:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger run -a silly -e TNK -c examples/silly_tnk.yaml -v 2\n"})}),"\n",(0,s.jsx)(n.p,{children:"The table would look like:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{children:"|    iter    |     c1     |     x2     |\n----------------------------------------\n|  1         |  3.73      |  2.198     |\n|  2         | -0.9861    |  0.3375    |\n|  3         |  1.888     |  1.729     |\n|  4         |  2.723     |  1.955     |\n|  5         | -1.092     |  0.08923   |\n|  6         |  1.357     |  1.568     |\n|  7         |  4.559     |  2.379     |\n|  8         |  8.757     |  3.14      |\n|  9         |  2.957     |  2.014     |\n|  10        |  0.1204    |  1.105     |\n|  11        |  2.516     |  1.902     |\n|  12        | -0.01194   |  1.043     |\n|  13        |  7.953     |  3.009     |\n|  14        | -1.095     |  0.07362   |\n|  15        | -0.3229    |  0.8815    |\n|  16        | -1.096     |  0.06666   |\n|  17        |  2.662     |  1.94      |\n|  18        |  6.987     |  2.844     |\n|  19        | -0.9734    |  0.3558    |\n|  20        |  3.694     |  2.19      |\n|  21        | -1.032     |  0.2613    |\n|  22        |  2.441     |  1.882     |\n|  23        |  7.042     |  2.853     |\n|  24        |  4.682     |  2.405     |\n|  25        |  0.5964    |  1.302     |\n|  26        |  0.3664    |  1.211     |\n|  27        |  1.966     |  1.751     |\n|  28        |  0.2181    |  1.148     |\n|  29        |  7.954     |  3.009     |\n|  30        | -0.8986    |  0.4488    |\n|  31        | -0.7536    |  0.5885    |\n|  32        |  3.602     |  2.168     |\n|  33        |  0.5527    |  1.286     |\n|  34        | -0.6969    |  0.6349    |\n|  35        | -1.094     |  0.07974   |\n|  36        | -0.8758    |  0.4735    |\n|  37        |  5.995     |  2.664     |\n|  38        |  3.638     |  2.177     |\n|  39        |  2.489     |  1.895     |\n|  40        |  0.8434    |  1.394     |\n|  41        |  0.4919    |  1.262     |\n|  42        | -0.4929    |  0.7792    |\n========================================\n"})}),"\n",(0,s.jsx)(n.p,{children:"Verbose level 1 only prints out the optimal solutions along the run:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger run -a silly -e TNK -c examples/silly_tnk.yaml -v 1\n"})}),"\n",(0,s.jsx)(n.p,{children:"The table would look like:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{children:"|    iter    |     c1     |     x2     |\n----------------------------------------\n|  1         |  1.96      |  1.749     |\n|  2         | -1.037     |  0.2518    |\n|  18        | -1.1       |  0.01942   |\n========================================\n"})}),"\n",(0,s.jsx)(n.p,{children:"Verbose level 0 turns off the printing feature completely:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger run -a silly -e TNK -c examples/silly_tnk.yaml -v 0\n"})}),"\n",(0,s.jsx)(n.p,{children:"The table would not be printed."}),"\n",(0,s.jsx)(n.h3,{id:"configure-algorithmenvironment-parameters",children:"Configure algorithm/environment parameters"}),"\n",(0,s.jsx)(n.p,{children:"The following two commands show how to config parameters of the algorithm/environment."}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:'badger run -a silly -ap "dimension: 4" -e dumb -c examples/silly_dumb.yaml\n'})}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:'badger run -a silly -ap "{dimension: 4, max_iter: 10}" -e dumb -c examples/silly_dumb.yaml\n'})}),"\n",(0,s.jsx)(n.h3,{id:"run-with-algorithms-provided-by-extensions",children:"Run with algorithms provided by extensions"}),"\n",(0,s.jsxs)(n.p,{children:["In order to run the following command, you'll need to ",(0,s.jsx)(n.a,{href:"https://github.com/ChristopherMayes/Xopt#installing-xopt",children:"set up xopt"})," on your computer (since the algorithms are provided by xopt)."]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:'badger run -a cnsga -ap "max_generations: 10" -e TNK -c examples/cnsga_tnk.yaml\n'})}),"\n",(0,s.jsx)(n.h3,{id:"save-a-run",children:"Save a run"}),"\n",(0,s.jsxs)(n.p,{children:["To save a routine to database in ",(0,s.jsx)(n.code,{children:"$BADGER_DB_ROOT"}),", just add the ",(0,s.jsx)(n.code,{children:"-s [SAVE_NAME]"})," option. This command will run and save the routine with a randomly generated two-word name:"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger run -a silly -e TNK -c examples/silly_tnk.yaml -s\n"})}),"\n",(0,s.jsxs)(n.p,{children:["The following command will run the routine and save it as ",(0,s.jsx)(n.code,{children:"test_routine"}),":"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger run -a silly -e TNK -c examples/silly_tnk.yaml -s test_routine\n"})}),"\n",(0,s.jsx)(n.h2,{id:"rerun-a-saved-optimization-routine",children:"Rerun a saved optimization routine"}),"\n",(0,s.jsxs)(n.p,{children:["Say we have the routine ",(0,s.jsx)(n.code,{children:"test_routine"})," saved. List all the saved routines by:"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger routine\n"})}),"\n",(0,s.jsxs)(n.p,{children:["To get the details of some specific routine (say, ",(0,s.jsx)(n.code,{children:"test_routine"}),"):"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger routine test_routine\n"})}),"\n",(0,s.jsx)(n.p,{children:"To rerun it, do:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger routine test_routine -r\n"})}),"\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.code,{children:"badger routine"})," also supports the ",(0,s.jsx)(n.code,{children:"-y"})," and ",(0,s.jsx)(n.code,{children:"-v"})," options, as ",(0,s.jsx)(n.code,{children:"badger run"})," does."]}),"\n",(0,s.jsx)(n.h2,{id:"configure-badger",children:"Configure Badger"}),"\n",(0,s.jsxs)(n.p,{children:["If you would like to change some setting that you configured during the first time you run ",(0,s.jsx)(n.code,{children:"badger"}),", you could do so with ",(0,s.jsx)(n.code,{children:"badger config"}),"."]}),"\n",(0,s.jsx)(n.p,{children:"List all the configurations:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger config\n"})}),"\n",(0,s.jsx)(n.p,{children:"To config a property:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"badger config KEY\n"})}),"\n",(0,s.jsxs)(n.p,{children:["Where ",(0,s.jsx)(n.code,{children:"KEY"})," is one of the keys in the configuration list."]}),"\n",(0,s.jsx)(n.h2,{id:"launch-the-badger-gui",children:"Launch the Badger GUI"}),"\n",(0,s.jsx)(n.p,{children:"Badger supports a GUI mode. You can launch the GUI by:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{children:"badger -g\n"})})]})}function h(e={}){const{wrapper:n}={...(0,a.a)(),...e.components};return n?(0,s.jsx)(n,{...e,children:(0,s.jsx)(c,{...e})}):c(e)}},1151:(e,n,i)=>{i.d(n,{Z:()=>o,a:()=>l});var s=i(7294);const a={},r=s.createContext(a);function l(e){const n=s.useContext(r);return s.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function o(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(a):e.components||a:l(e.components),s.createElement(r.Provider,{value:n},e.children)}}}]);