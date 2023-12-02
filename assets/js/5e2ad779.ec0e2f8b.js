"use strict";(self.webpackChunkbadger_home=self.webpackChunkbadger_home||[]).push([[3061],{5787:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>s,default:()=>d,frontMatter:()=>r,metadata:()=>a,toc:()=>h});var i=n(5893),o=n(1151);const r={sidebar_position:3},s="GUI Usage",a={id:"guides/gui-usage",title:"GUI Usage",description:"Once you launch Badger in GUI mode, you'll have various Badger features to explore. You can search through this page to get to the guide on any specify GUI feature, or if you believe a guide is missing for the topic you are interested in, please consider raising an issue here or shooting us an email, many thanks :)",source:"@site/docs/guides/gui-usage.md",sourceDirName:"guides",slug:"/guides/gui-usage",permalink:"/Badger/docs/next/guides/gui-usage",draft:!1,unlisted:!1,editUrl:"https://github.com/SLAC-ML/Badger-Home/edit/master/docs/guides/gui-usage.md",tags:[],version:"current",sidebarPosition:3,frontMatter:{sidebar_position:3},sidebar:"tutorialSidebar",previous:{title:"CLI Usage",permalink:"/Badger/docs/next/guides/cli-usage"},next:{title:"Create a plugin",permalink:"/Badger/docs/next/guides/create-a-plugin"}},l={},h=[{value:"Home page",id:"home-page",level:2},{value:"Create a new routine",id:"create-a-new-routine",level:3},{value:"Select/deselect a routine",id:"selectdeselect-a-routine",level:3},{value:"Edit a routine",id:"edit-a-routine",level:3},{value:"Delete a routine",id:"delete-a-routine",level:3},{value:"Filter routines",id:"filter-routines",level:3},{value:"Browse the historical runs",id:"browse-the-historical-runs",level:3},{value:"Configure Badger settings",id:"configure-badger-settings",level:3},{value:"Export/import routines",id:"exportimport-routines",level:3},{value:"Run monitor",id:"run-monitor",level:2},{value:"Control an optimization run",id:"control-an-optimization-run",level:3},{value:"Set termination condition",id:"set-termination-condition",level:3},{value:"Reset the environment",id:"reset-the-environment",level:3},{value:"Inspect the solutions in a run",id:"inspect-the-solutions-in-a-run",level:3},{value:"Jump to the optimal solution",id:"jump-to-the-optimal-solution",level:3},{value:"Dial in the selected solution",id:"dial-in-the-selected-solution",level:3},{value:"Change the horizontal axis",id:"change-the-horizontal-axis",level:3},{value:"Normalize the variables for better visualization",id:"normalize-the-variables-for-better-visualization",level:3},{value:"Delete a run",id:"delete-a-run",level:3},{value:"Send record to logbook",id:"send-record-to-logbook",level:3},{value:"Use data analysis/visualization extensions",id:"use-data-analysisvisualization-extensions",level:3},{value:"Routine editor",id:"routine-editor",level:2},{value:"Set the metadata",id:"set-the-metadata",level:3},{value:"Select and configure the generator",id:"select-and-configure-the-generator",level:3},{value:"Select and configure the environment",id:"select-and-configure-the-environment",level:3},{value:"Configure the VOCS",id:"configure-the-vocs",level:3}];function c(e){const t={a:"a",admonition:"admonition",code:"code",em:"em",h1:"h1",h2:"h2",h3:"h3",img:"img",li:"li",ol:"ol",p:"p",section:"section",strong:"strong",sup:"sup",ul:"ul",...(0,o.a)(),...e.components};return(0,i.jsxs)(i.Fragment,{children:[(0,i.jsx)(t.h1,{id:"gui-usage",children:"GUI Usage"}),"\n",(0,i.jsxs)(t.p,{children:["Once you launch Badger in GUI mode, you'll have various Badger features to explore. You can search through this page to get to the guide on any specify GUI feature, or if you believe a guide is missing for the topic you are interested in, please consider ",(0,i.jsx)(t.a,{href:"https://github.com/slaclab/Badger/issues/new",children:"raising an issue here"})," or ",(0,i.jsx)(t.a,{href:"mailto:zhezhang@slac.stanford.edu",children:"shooting us an email"}),", many thanks :)"]}),"\n",(0,i.jsx)(t.h2,{id:"home-page",children:"Home page"}),"\n",(0,i.jsx)(t.h3,{id:"create-a-new-routine",children:"Create a new routine"}),"\n",(0,i.jsxs)(t.p,{children:["On Badger home page, click the ",(0,i.jsx)(t.em,{children:"Plus"})," button (highlighted in the screenshot below):"]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Create new routine",src:n(4245).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.p,{children:"You'll land on the routine editor page:"}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Routine editor",src:n(5302).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.p,{children:"where you can select the generator to use, the environment to optimize on, and configure the VOCS."}),"\n",(0,i.jsx)(t.h3,{id:"selectdeselect-a-routine",children:"Select/deselect a routine"}),"\n",(0,i.jsx)(t.p,{children:"Hover one item in the routine list (highlighted below) and click it will select the specific routine:"}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Hover on routine",src:n(351).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsxs)(t.p,{children:["Once selected, the content in the ",(0,i.jsx)(t.a,{href:"#browse-the-historical-runs",children:"history browser"})," (on top of the run monitor) will change to show the runs corresponding to the selected routine only."]}),"\n",(0,i.jsx)(t.p,{children:"Click the selected routine again to deselect it. If no routine is selected, the history browser will show all the runs for all the routines."}),"\n",(0,i.jsx)(t.h3,{id:"edit-a-routine",children:"Edit a routine"}),"\n",(0,i.jsxs)(t.p,{children:["After ",(0,i.jsx)(t.a,{href:"#selectdeselect-a-routine",children:"select a routine"}),", click the ",(0,i.jsx)(t.em,{children:"Routine Editor"})," tab on top of the ",(0,i.jsx)(t.a,{href:"#run-monitor",children:"run monitor"}),", you'll be able to edit the routine and save the changes."]}),"\n",(0,i.jsxs)(t.admonition,{type:"tip",children:[(0,i.jsx)(t.p,{children:"One important/counterintuitive thing to keep in mind though, is that in Badger, if you have at least one run associates with the routine, you cannot edit and save the changed under the same routine name, you'll have to give the edited routine a new name. This behavior is to guarantee that each run can be mapped to the correct routine by the time it was run."}),(0,i.jsx)(t.p,{children:"Of course, if there are no runs associate with the routine, you can edit and rename it just fine."})]}),"\n",(0,i.jsx)(t.h3,{id:"delete-a-routine",children:"Delete a routine"}),"\n",(0,i.jsxs)(t.p,{children:["Hover the ",(0,i.jsx)(t.em,{children:"Delete"})," button (the one with the trash can icon) on the routine you'd like to delete will highlight it in red, click the button and confirm on the confirmation dialog will delete the routine."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Delete a routine",src:n(6169).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsxs)(t.p,{children:["Note that deleting a routine will ",(0,i.jsx)(t.strong,{children:"NOT"})," automatically delete all the runs associate with it. This behavior is intended to give users a chance to recover it if regretted later. Of course, if all the associated runs have already been deleted, then it will not be possible to recover the routine -- nevertheless you can ",(0,i.jsx)(t.a,{href:"#create-a-new-routine",children:"recreate it"}),", creating a routine is not that hard after all."]}),"\n",(0,i.jsx)(t.h3,{id:"filter-routines",children:"Filter routines"}),"\n",(0,i.jsx)(t.p,{children:"You can use the search bar to filter the routines. Badger will try to match the routine names with the text you put in the search bar. Currently we don't support RegEx, but we plan to add the support in the future releases, along with the ability to search other metadata, such as descriptions."}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Filter routines",src:n(2441).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.h3,{id:"browse-the-historical-runs",children:"Browse the historical runs"}),"\n",(0,i.jsxs)(t.p,{children:["You can browse the historical runs in Badger by clicking the ",(0,i.jsx)(t.em,{children:"Next"}),"/",(0,i.jsx)(t.em,{children:"Previous"})," buttons in the history browser:"]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"History browser",src:n(193).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.p,{children:"or simply click on the combobox that shows the current run name, to trigger a dropdown menu that lists all the matched runs (categorized and sorted by run date and time). Clicking on a run in the menu will show the run data in the run monitor below."}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"History dropdown",src:n(937).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.p,{children:"Note that the routine editor content will also be refreshed according to routine of the selected run."}),"\n",(0,i.jsx)(t.h3,{id:"configure-badger-settings",children:"Configure Badger settings"}),"\n",(0,i.jsxs)(t.p,{children:["Click the ",(0,i.jsx)(t.em,{children:"Settings"})," button (with the little gear icon) on the bottom right of the Badger GUI will bring up the Badger settings dialog, where you can configure Badger as needed:"]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Configure Badger",src:n(2124).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsxs)(t.p,{children:["As a side note, the routine name for the current run shown in the run monitor is displayed besides the ",(0,i.jsx)(t.em,{children:"Settings"})," button."]}),"\n",(0,i.jsx)(t.h3,{id:"exportimport-routines",children:"Export/import routines"}),"\n",(0,i.jsxs)(t.p,{children:["Click the ",(0,i.jsx)(t.em,{children:"Export"}),"/",(0,i.jsx)(t.em,{children:"Import"})," button below the routine list will let you export the ",(0,i.jsxs)(t.a,{href:"#filter-routines",children:[(0,i.jsx)(t.strong,{children:"FILTERED"})," routines"]})," as a ",(0,i.jsx)(t.code,{children:".db"})," file or import the routines in a ",(0,i.jsx)(t.code,{children:".db"})," file."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Export/import routines",src:n(1144).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.h2,{id:"run-monitor",children:"Run monitor"}),"\n",(0,i.jsx)(t.h3,{id:"control-an-optimization-run",children:"Control an optimization run"}),"\n",(0,i.jsx)(t.p,{children:"Start an optimization run by either:"}),"\n",(0,i.jsxs)(t.ul,{children:["\n",(0,i.jsxs)(t.li,{children:[(0,i.jsx)(t.a,{href:"#selectdeselect-a-routine",children:"Select a routine"})," and click the green ",(0,i.jsx)(t.em,{children:"Run/Stop"})," button (with the play icon), or"]}),"\n",(0,i.jsxs)(t.li,{children:[(0,i.jsx)(t.a,{href:"#browse-the-historical-runs",children:"Browse the historical runs"})," and select the one you'd like to rerun, then click the ",(0,i.jsx)(t.em,{children:"Run/Stop"})," button"]}),"\n"]}),"\n",(0,i.jsx)(t.admonition,{type:"tip",children:(0,i.jsxs)(t.p,{children:["Note that for the second approach, Badger simply uses the routine that drove the selected historical run to run the new round of optimization. It does ",(0,i.jsx)(t.strong,{children:"NOT"})," continue the old run. That being said, the continue old run feature is planned for future releases of Badger."]})}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Control a run",src:n(7202).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsxs)(t.p,{children:["To pause the run, click the ",(0,i.jsx)(t.em,{children:"Pause/Resume"})," button to the right of the ",(0,i.jsx)(t.em,{children:"Run/Stop"})," button. To resume a paused run, click the ",(0,i.jsx)(t.em,{children:"Pause/Resume"})," button again."]}),"\n",(0,i.jsxs)(t.p,{children:["Click the ",(0,i.jsx)(t.em,{children:"Run/Stop"})," button again (turned red once the run started) to stop the run."]}),"\n",(0,i.jsx)(t.h3,{id:"set-termination-condition",children:"Set termination condition"}),"\n",(0,i.jsxs)(t.p,{children:["Click the small dropdown arrow on the ",(0,i.jsx)(t.em,{children:"Run/Stop"})," button to open the run menu, select ",(0,i.jsx)(t.em,{children:"Run until"}),", then configure the termination condition and run the optimization. The run will be terminated once the terminaton condition is met."]}),"\n",(0,i.jsx)(t.p,{children:"Currently Badger supports two types of termination conditions:"}),"\n",(0,i.jsxs)(t.ul,{children:["\n",(0,i.jsx)(t.li,{children:"Terminate when maximum evaluation reached, or"}),"\n",(0,i.jsx)(t.li,{children:"Terminate when maximum running time exceeded"}),"\n"]}),"\n",(0,i.jsx)(t.p,{children:"The convergence-based termination condition will be added soon."}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Set termination condition",src:n(1817).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.admonition,{type:"tip",children:(0,i.jsxs)(t.p,{children:["Once you select the ",(0,i.jsx)(t.em,{children:"Run until"})," action, the default behavior of the green ",(0,i.jsx)(t.em,{children:"Run/Stop"})," button will change accordingly. The default behavior (",(0,i.jsx)(t.em,{children:"Run"}),", or ",(0,i.jsx)(t.em,{children:"Run until"}),") will be reset to ",(0,i.jsx)(t.em,{children:"Run"})," (means run forever) when Badger GUI is closed."]})}),"\n",(0,i.jsx)(t.p,{children:"For now, you can only use single termination condition. Multiple termination rules will be supported in the future."}),"\n",(0,i.jsx)(t.h3,{id:"reset-the-environment",children:"Reset the environment"}),"\n",(0,i.jsxs)(t.p,{children:["You can reset the environment to initial states after a run by clicking the ",(0,i.jsx)(t.em,{children:"Reset"})," button. Note that you can only reset the environment that you just run, and you cannot reset the environment in the middle of a run. To achieve the latter, ",(0,i.jsx)(t.a,{href:"#control-an-optimization-run",children:"terminate the run"})," first and then reset."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Reset the env",src:n(7202).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.h3,{id:"inspect-the-solutions-in-a-run",children:"Inspect the solutions in a run"}),"\n",(0,i.jsx)(t.p,{children:"You can either drag the yellow inspector line (the position will be synced across all monitors), or click inside the monitor, to select the solution you are interested in."}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Inspect solutions",src:n(849).Z+"",width:"2784",height:"2078"})}),"\n",(0,i.jsx)(t.p,{children:"The know the exact values of the variables/objectives of that solution, drag the horizontal handle below the action buttons up to open the data table, the solution selected on the monitor will be highlighted in the data table. You can select any region of the table and copy the data as you do in Excel sheets."}),"\n",(0,i.jsx)(t.h3,{id:"jump-to-the-optimal-solution",children:"Jump to the optimal solution"}),"\n",(0,i.jsxs)(t.p,{children:["Click the star button to select the optimal solution according to the VOCS. Note that this action only selects the optimum, it does ",(0,i.jsx)(t.strong,{children:"NOT"})," set the environment with the selected solution. To dial in the optimal solution, ",(0,i.jsx)(t.a,{href:"#dial-in-the-selected-solution",children:"perform the dial in action"}),"."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Jump to optimum",src:n(5211).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.h3,{id:"dial-in-the-selected-solution",children:"Dial in the selected solution"}),"\n",(0,i.jsxs)(t.p,{children:["You can dial in any selected solution by clicking the ",(0,i.jsx)(t.em,{children:"Dial-in"})," button (with the right-down arrow icon) besides the star button. A confirmation dialog will be popped up to give you a heads-up, in case that you click the button by accident (could be dangerous when you are using Badger to optimize a real machine!)."]}),"\n",(0,i.jsx)(t.h3,{id:"change-the-horizontal-axis",children:"Change the horizontal axis"}),"\n",(0,i.jsxs)(t.p,{children:["You can show the run on iteration-based x-axis or time-based x-axis. Simply select the desired x-axis type (",(0,i.jsx)(t.code,{children:"Iteration"})," or ",(0,i.jsx)(t.code,{children:"Time"}),") in the ",(0,i.jsx)(t.em,{children:"X Axis"})," dropdown menu in the visualization configuration bar highlighted below."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Configure visualization options",src:n(5338).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.admonition,{type:"tip",children:(0,i.jsx)(t.p,{children:"You can configure the visualization options anytime, in the middle of a run or not."})}),"\n",(0,i.jsx)(t.h3,{id:"normalize-the-variables-for-better-visualization",children:"Normalize the variables for better visualization"}),"\n",(0,i.jsxs)(t.p,{children:["Sometimes it's convinient to show the variables in a normalized manner, so that you can observe all trends in the same frame. You can do that by selecting ",(0,i.jsx)(t.code,{children:"Normalized"})," in the ",(0,i.jsx)(t.em,{children:"Y Axis (Var)"})," dropdown menu. Check the ",(0,i.jsx)(t.em,{children:"Relative"})," checkbox would show the variable changes relative to its initial value, you can combine the ",(0,i.jsx)(t.em,{children:"Y Axis (Var)"})," options and the ",(0,i.jsx)(t.em,{children:"Relative"})," options to fit the visualization to your own needs."]}),"\n",(0,i.jsx)(t.h3,{id:"delete-a-run",children:"Delete a run"}),"\n",(0,i.jsxs)(t.p,{children:["Click the red ",(0,i.jsx)(t.em,{children:"Delete run"})," button (trash bin icon) at the bottom right of the run monitor to delete the current run shown on the run monitor. You'll be asked to confirm the delete action."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Delete a run",src:n(8064).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.h3,{id:"send-record-to-logbook",children:"Send record to logbook"}),"\n",(0,i.jsxs)(t.p,{children:["To send a log entry to the logbook directory",(0,i.jsx)(t.sup,{children:(0,i.jsx)(t.a,{href:"#user-content-fn-logdir",id:"user-content-fnref-logdir","data-footnote-ref":!0,"aria-describedby":"footnote-label",children:"1"})}),", click the blue button besides the ",(0,i.jsxs)(t.a,{href:"#delete-a-run",children:[(0,i.jsx)(t.em,{children:"Delete run"})," button"]}),"."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Logbook and extension",src:n(1431).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.p,{children:"The log entry will include a screenshot of the run monitor and an xml file that summarizes the optimization run."}),"\n",(0,i.jsx)(t.admonition,{type:"tip",children:(0,i.jsx)(t.p,{children:"Currently the log entry format is fixed. Flexible/customizable log entry support will be added in the future releases of Badger."})}),"\n",(0,i.jsx)(t.h3,{id:"use-data-analysisvisualization-extensions",children:"Use data analysis/visualization extensions"}),"\n",(0,i.jsxs)(t.p,{children:["You can open the extension menu by clicking the green ",(0,i.jsx)(t.em,{children:"Extension"})," button besides the ",(0,i.jsxs)(t.a,{href:"#send-record-to-logbook",children:[(0,i.jsx)(t.em,{children:"Logbook"})," button"]}),". Extensions in Badger provides capibilities more than simply monitoring the optimization curves. Extensions could parse the Gaussian model performance on the fly during the run, visualize the Pareto front in a multi-objective optimization, give insight on tuning knobs sensitivities wrt the objective, etc. Currently we have the following extensions shipped with Badger:"]}),"\n",(0,i.jsxs)(t.ul,{children:["\n",(0,i.jsx)(t.li,{children:"Pareto front viewer"}),"\n"]}),"\n",(0,i.jsx)(t.p,{children:"We plan to implement the extension system in a similar manner to the plugin system in Badger, so that each extension could be developed, maintained, and installed separately, for maximum flexibility and extensibility."}),"\n",(0,i.jsx)(t.h2,{id:"routine-editor",children:"Routine editor"}),"\n",(0,i.jsx)(t.p,{children:"Routine editor enables the users to create/edit/save the routine easily. Below is a simple guide on the main features of the routine editor."}),"\n",(0,i.jsx)(t.h3,{id:"set-the-metadata",children:"Set the metadata"}),"\n",(0,i.jsxs)(t.p,{children:["Metadata of a routine contains the name and the description of the routine. You can change the description of a routine anytime by editing the content then clicking the ",(0,i.jsx)(t.em,{children:"Update"})," button. Note that if you are creating a new routine then you don't have to click the ",(0,i.jsx)(t.em,{children:"Update"})," button, since the metadata will be saved once you save the whole routine."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Set metadata",src:n(5412).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.h3,{id:"select-and-configure-the-generator",children:"Select and configure the generator"}),"\n",(0,i.jsxs)(t.p,{children:["To configure the generator in a routine, click the generator selector in the ",(0,i.jsx)(t.em,{children:"Algorithm"})," section, then edit the generator parameters in the ",(0,i.jsx)(t.em,{children:"Params"})," text box. Usually you don't need to change anything in the generator parameters -- the default values should work well for most cases."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Set generator",src:n(82).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsxs)(t.p,{children:["You can check the docs for the selected generator by clicking the ",(0,i.jsx)(t.em,{children:"Open Docs"})," button."]}),"\n",(0,i.jsx)(t.h3,{id:"select-and-configure-the-environment",children:"Select and configure the environment"}),"\n",(0,i.jsxs)(t.p,{children:["To configure the environment in a routine, click the environment selector in the ",(0,i.jsx)(t.em,{children:"Environment + VOCS"})," section, then edit the environment parameters (if any) in the ",(0,i.jsx)(t.em,{children:"Params"})," text box."]}),"\n",(0,i.jsx)(t.p,{children:(0,i.jsx)(t.img,{alt:"Set environment",src:n(302).Z+"",width:"2784",height:"1720"})}),"\n",(0,i.jsx)(t.h3,{id:"configure-the-vocs",children:"Configure the VOCS"}),"\n",(0,i.jsxs)(t.p,{children:["The VOCS configuration panel is right below the environment configuration panel. It has 3 parts: variables configuration, objectives configuration, and constraints/states configurations (under the ",(0,i.jsx)(t.em,{children:"More"})," subsection)."]}),"\n",(0,i.jsxs)(t.p,{children:["On the variables configuration panel, you can filter the variables in the selected environment by its name, note that RegEx is supported here. For example, you can enter something like ",(0,i.jsx)(t.code,{children:"Q[1-4]*"})," to match the variables start with ",(0,i.jsx)(t.code,{children:"Q1"}),", ",(0,i.jsx)(t.code,{children:"Q2"}),", ",(0,i.jsx)(t.code,{children:"Q3"}),", and ",(0,i.jsx)(t.code,{children:"Q4"}),"."]}),"\n",(0,i.jsxs)(t.p,{children:["You can check the checkbox in front of each variable to include it in the optimization. Variables that are not selected will ",(0,i.jsx)(t.strong,{children:"NOT"})," be tuned during the run! You'll need to check at least one variable to make a valid routine."]}),"\n",(0,i.jsx)(t.admonition,{type:"tip",children:(0,i.jsxs)(t.p,{children:["Click on the left-most blank cell in the variable table header (the one on top of all the variable checkboxes, besides the ",(0,i.jsx)(t.em,{children:"Name"})," header cell) will check/uncheck all the filtered variables (all variables that shown in the table when the ",(0,i.jsx)(t.em,{children:"Show Checked Only"})," checkbox is unchecked)."]})}),"\n",(0,i.jsx)("p",{align:"center",children:(0,i.jsx)("img",{alt:"Configure variables",src:n(3137).Z,style:{width:"70%"}})}),"\n",(0,i.jsxs)(t.p,{children:["Check the ",(0,i.jsx)(t.em,{children:"Show Checked Only"})," checkbox to only show the variables that would join the optimization."]}),"\n",(0,i.jsxs)(t.p,{children:["The ",(0,i.jsx)(t.em,{children:"Min"})," and ",(0,i.jsx)(t.em,{children:"Max"})," columns in the variable table show the hard limit",(0,i.jsx)(t.sup,{children:(0,i.jsx)(t.a,{href:"#user-content-fn-hard-lim",id:"user-content-fnref-hard-lim","data-footnote-ref":!0,"aria-describedby":"footnote-label",children:"2"})})," of each variable (defined in the environment, usually limited by hardware). You can change the values in those two columns to adjust the variable ranges that you'd like to use in the optimization (say, you would like to start out conservatively -- so the variables should only change within 10% of the whole tunable ranges)."]}),"\n",(0,i.jsx)(t.admonition,{type:"tip",children:(0,i.jsxs)(t.p,{children:["You can also limit the variable ranges by clicking the ",(0,i.jsx)(t.em,{children:"Limit Variable Range"})," button, it will give you options to limit all the selected variables ranges by percentage wrt their current values or the full tunable ranges in one go."]})}),"\n",(0,i.jsxs)(t.p,{children:["Then you'll want to set the initial points (from which solutions the optimization would start), you can do it by edit the table under the ",(0,i.jsx)(t.em,{children:"Initial Points"})," subsection. One common scenario is to start the optimization from the current solution, you can do that by clicking the ",(0,i.jsx)(t.em,{children:"Add Current"})," button, this will insert the current solution to the initial points table."]}),"\n",(0,i.jsxs)(t.p,{children:["Now we can go ahead and configure the objectives. It's very similar to the variables configuration, the main difference is that this time you'll need to specific the rule",(0,i.jsx)(t.sup,{children:(0,i.jsx)(t.a,{href:"#user-content-fn-rule",id:"user-content-fnref-rule","data-footnote-ref":!0,"aria-describedby":"footnote-label",children:"3"})})," of each objective."]}),"\n",(0,i.jsx)("p",{align:"center",children:(0,i.jsx)("img",{alt:"Configure objectives",src:n(1469).Z,style:{width:"70%"}})}),"\n",(0,i.jsxs)(t.p,{children:["If needed, you can add constraints and states",(0,i.jsx)(t.sup,{children:(0,i.jsx)(t.a,{href:"#user-content-fn-states",id:"user-content-fnref-states","data-footnote-ref":!0,"aria-describedby":"footnote-label",children:"4"})})," to the routine by configuring them in the expanded ",(0,i.jsx)(t.em,{children:"More"})," subsection. For constraints, check the ",(0,i.jsx)(t.em,{children:"Critical"})," checkbox would mark the corresponding constraint as a critical one, that would pause the optimization immediately once violated."]}),"\n",(0,i.jsx)(t.admonition,{type:"caution",children:(0,i.jsxs)(t.p,{children:["For the non-critical constraints, violations will ",(0,i.jsx)(t.strong,{children:"NOT"})," trigger a pause in a run, and it might not affect the optimization behavior at all if the chosen generator (say, ",(0,i.jsx)(t.code,{children:"neldermead"}),(0,i.jsx)(t.sup,{children:(0,i.jsx)(t.a,{href:"#user-content-fn-simplex",id:"user-content-fnref-simplex","data-footnote-ref":!0,"aria-describedby":"footnote-label",children:"5"})}),") doesn't support constraints."]})}),"\n",(0,i.jsx)("p",{align:"center",children:(0,i.jsx)("img",{alt:"Configure constraints and states",src:n(76).Z,style:{width:"70%"}})}),"\n",(0,i.jsxs)(t.section,{"data-footnotes":!0,className:"footnotes",children:[(0,i.jsx)(t.h2,{className:"sr-only",id:"footnote-label",children:"Footnotes"}),"\n",(0,i.jsxs)(t.ol,{children:["\n",(0,i.jsxs)(t.li,{id:"user-content-fn-logdir",children:["\n",(0,i.jsxs)(t.p,{children:["Logbook directory is one of the configurations in Badger. You can check the current setting by running ",(0,i.jsx)(t.code,{children:"badger config"})," in terminal, then check the value of the ",(0,i.jsx)(t.code,{children:"BADGER_LOGBOOK_ROOT"})," key ",(0,i.jsx)(t.a,{href:"#user-content-fnref-logdir","data-footnote-backref":"","aria-label":"Back to reference 1",className:"data-footnote-backref",children:"\u21a9"})]}),"\n"]}),"\n",(0,i.jsxs)(t.li,{id:"user-content-fn-hard-lim",children:["\n",(0,i.jsxs)(t.p,{children:["Those are ranges that should never be violated, no matter how the routine would be configured ",(0,i.jsx)(t.a,{href:"#user-content-fnref-hard-lim","data-footnote-backref":"","aria-label":"Back to reference 2",className:"data-footnote-backref",children:"\u21a9"})]}),"\n"]}),"\n",(0,i.jsxs)(t.li,{id:"user-content-fn-rule",children:["\n",(0,i.jsxs)(t.p,{children:["Direction of the optimization, either ",(0,i.jsx)(t.code,{children:"MAXIMIZE"})," or ",(0,i.jsx)(t.code,{children:"MINIMIZE"})," ",(0,i.jsx)(t.a,{href:"#user-content-fnref-rule","data-footnote-backref":"","aria-label":"Back to reference 3",className:"data-footnote-backref",children:"\u21a9"})]}),"\n"]}),"\n",(0,i.jsxs)(t.li,{id:"user-content-fn-states",children:["\n",(0,i.jsxs)(t.p,{children:["Variables or observables that you'd like to monitor during the run, but won't join the run directly ",(0,i.jsx)(t.a,{href:"#user-content-fnref-states","data-footnote-backref":"","aria-label":"Back to reference 4",className:"data-footnote-backref",children:"\u21a9"})]}),"\n"]}),"\n",(0,i.jsxs)(t.li,{id:"user-content-fn-simplex",children:["\n",(0,i.jsxs)(t.p,{children:["Aka Simplex ",(0,i.jsx)(t.a,{href:"#user-content-fnref-simplex","data-footnote-backref":"","aria-label":"Back to reference 5",className:"data-footnote-backref",children:"\u21a9"})]}),"\n"]}),"\n"]}),"\n"]})]})}function d(e={}){const{wrapper:t}={...(0,o.a)(),...e.components};return t?(0,i.jsx)(t,{...e,children:(0,i.jsx)(c,{...e})}):c(e)}},76:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/const-5bcaffaebb43bd3cfbb4aef21f15c72a.png"},1469:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/obj-ef68266ca3f6f3b8ccf096262469853c.png"},3137:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/var-d822f4429c98425f996d18ab63869003.png"},7202:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/control-6093247235285dea876d9f78db347659.png"},4245:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/create_new_routine-56ddde3bb0995b5fd4737de09fccedc2.png"},1431:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/ctrl_misc-045bc1ef53442a1bfe2b1b6edaf9e276.png"},6169:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/delete_routine-f4138a20ffb79f2d80f4017ac4ce429c.png"},8064:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/delete_run-c7585c42abc4d891d72c824cb261da5a.png"},1144:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/export_import_routines-73fe50b02fb2177b5ab579d15e180de9.png"},2441:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/filter_routines-79766aa9181762ebed1e2198ce343f1c.png"},193:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/history_browser-9fcbac20951a9465229be19606ccb3c3.png"},937:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/history_dropdown-47eebf0e6413f150ccfe28e222bf3805.png"},351:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/hover_on_routine-c36631e9d274acab130661e66217f631.png"},849:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/inspect_sol-882235e407931101b2ac34456221c4f2.png"},5211:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/jump_to_opt-f6d0f7a9cde9986021152fb9d6499b0e.png"},5302:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/routine_editor-cb93cadbd434db75fb4244dd81e7f034.png"},302:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/set_env-2eca47029e68a10e40289efebf20a61e.png"},82:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/set_gen-1d96ad5a85afdfc4777213499c57fe69.png"},5412:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/set_meta-ebb3a23dae9a4d4f4d60904eaa3277a1.png"},2124:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/settings-6f10cc35e9b79d337b02bdddae093c78.png"},1817:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/tc-9b337fefa8578fbb81bd8e02eb9eb901.png"},5338:(e,t,n)=>{n.d(t,{Z:()=>i});const i=n.p+"assets/images/vis_options-43f4587e48e7e864f7c452507765e07a.png"},1151:(e,t,n)=>{n.d(t,{Z:()=>a,a:()=>s});var i=n(7294);const o={},r=i.createContext(o);function s(e){const t=i.useContext(r);return i.useMemo((function(){return"function"==typeof e?e(t):{...t,...e}}),[t,e])}function a(e){let t;return t=e.disableParentContext?"function"==typeof e.components?e.components(o):e.components||o:s(e.components),i.createElement(r.Provider,{value:t},e.children)}}}]);