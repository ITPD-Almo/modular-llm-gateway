# Week 6 meeting transcript

- **Date:** 2026-11-07.
- **Participants:** Ali12hamdan and Customer, the two speakers in the supplied transcript.
- **Source:** the transcript the Customer sent after the call, cleaned for readability; false starts, filler words and repeated acknowledgments are reduced without changing substantive meaning. Narration while the demo was being set up that the automatic transcription did not capture intelligibly is marked `[unclear]` rather than reconstructed.
- **Sharing confirmation:** the team was told on 2026-11-08 that this de-identified transcript may be published and the recording shared with the instructors. The permission questions and answers are not captured in the source.
- **Time markers:** approximate elapsed minutes, shown as `[~HH:MM:00]`; exact recording timecodes and the recording link remain private.

[~00:00:00] Customer: It is up to you how you want to do it. What I have been telling other teams is that it would be good this semester for the team to come up with a method of interacting with the customer. I act as a customer, but I can give you feedback that customers usually will not give.
[~00:00:00] Customer: For example, a team yesterday decided among themselves to implement a feature. It was a good feature, but they just did it and I did not know about it. Customers usually either complain right away, saying they did not budget for it and it was not planned, or, even worse, they stay silent, hold a grudge later, and do not feel in control of the project.
[~00:01:00] Customer: So I am doing a balancing act: I let you go as you would, and I push you towards a more formal method of interacting with a customer. Right now we can do the review informally and improve it each time. Go ahead and show me what you were planning to do, what you have done, and go through the features.
[~00:01:00] Ali12hamdan: I can walk you through the issues we opened before and how the steps went. Let me share my screen. Can you see it?
[~00:02:00] Customer: Yes, I can see the screen.
[~00:02:00] Ali12hamdan: Your last comments were about testing and about installation: as a customer you need it to be easy to install. That was a good point and was not in our minds at the time. My part was to make it a one-line command that installs it as a tool on your system. For now it supports Linux and macOS, because they are very similar.
[~00:03:00] Ali12hamdan: We also have the safe plugin lifecycle events from before. Since I have DeepSeek API access, I refined the setup to accept a DeepSeek API key. We also added CI and made it deployable. We had a problem with the VM: we deployed on our own university-related VM, so I am not sure you will have full access to it, but as I understood our TA has no complaints.
[~00:04:00] Ali12hamdan: What I would like to do is show you how the plugin works for now. You requested something before, and we added it; I want to show it to you. One second.
[~00:05:00] Customer: You can just show me how I would install it. Run it in your terminal and show me how it works.
[~00:06:00] Ali12hamdan: I am setting up a VM for now. Can you see my terminal?
[~00:06:00] Customer: Yes.
[~00:06:00] Ali12hamdan: Since I have multiple versions of it, I have to install it in a specific way. As developers we have several versions installed, so we install it differently. Let me check one thing. [unclear] So, connect your own provider: for now just DeepSeek.
[~00:07:00] Customer: By DeepSeek, do you mean the DeepSeek harness or DeepSeek the model?
[~00:07:00] Ali12hamdan: The actual model API key.
[~00:07:00] Customer: Okay.
[~00:07:00] Ali12hamdan: I have this set up. Let me look for my key; maybe it expired. I will create a new one. [unclear]
[~00:08:00] Ali12hamdan: When you add an API key, you choose the Flash or the Pro model. The setup saves the key in a permission-protected local file, which is not encrypted; then you chat in another terminal, and it uses the DeepSeek balance. Then we go through removing the key and the running gateway. For now I added my key. We can send a demo request or use the actual provider. [unclear]
[~00:11:00] Customer: I do not know how close you are to actually running it. I am trying to see.
[~00:11:00] Ali12hamdan: I was looking for the exact demo that we have. [unclear] So, just a request. [unclear]
[~00:12:00] Customer: Let me give you a little feedback on what is going on. On one hand, it is cool that you connected to the actual LLM. You did not have to, but it is pretty nice.
[~00:12:00] Customer: I want to highlight that there are different types of customers depending on the product. Some customers have no idea about the technical part; others are more technically minded. This product is for DevOps people. Imagine that I am that DevOps person: your product needs to impress me as a DevOps person right away, so you need to align your features so that I say "that really helps".
[~00:14:00] Customer: So far, what I have seen is that you made a request to an LLM API. As a DevOps person I am not very impressed: I make a request, and so what? You need to structure your presentation and your features to address my pain points. I know it connects to an API eventually.
[~00:14:00] Customer: When we talked at the start about who this product is for, I outlined the pain points. The original idea was that it is for DevOps in a company where multiple developers or users need to talk to a cloud provider, and I have requirements from my security people, logging people and others, to make sure that what we do not want to get out does not get out. The idea was a gateway where you write all the boilerplate gateway logic and make it super easy for DevOps to add plugins, like a logging plugin.
[~00:16:00] Customer: Another team, for example, added a permission feature in the gateway itself, but it could have been just a plugin. The plugin itself is not interesting. What is interesting is the whole system: how to run it, how to run the plugins, what happens if I wrote a plugin incorrectly. Another team even tests for incorrect or malformed Python, or a plugin file that is too big.
[~00:17:00] Customer: As a DevOps person those features are very interesting to me, because I do not want to deal with them. I know I need those checks to make sure my plugins run, but I want to focus on the task at hand. Those features are interesting because the gateway does them, and they address the problem of the DevOps person in charge of providing a route from the company to a cloud provider.
[~00:18:00] Customer: So when you choose what to show, connecting to an LLM is nice, but it would be interesting to show other things, like deployment. That is another pain point we started with. Nowadays projects have a script that deploys them. You do not have to go to the one-line level, but it would be nice if you wrapped it all in a Docker container, or Docker Compose, so you do not have a bunch of environment settings flying around: a container that has all of it, whichever version you want to show. Bring it up and show me how it works. It should be super easy.
[~00:19:00] Customer: Then you do not need to deal with paths and versions. You can have fifty versions as different container versions and just run one. You are tapping into something DevOps people most likely already know; it is very well established. If you are comfortable with something else, Kubernetes for example, I am not saying you should do it, because it is a lot more complicated.
[~00:20:00] Ali12hamdan: Understood.
[~00:20:00] Customer: If you are familiar with it, do it that way, and tell me your assumption: they have Kubernetes, here is our system, and we manage the different versions. For this project you have to do some architecting of the system, because your customer is technical, and you need to tailor your features to that technical customer's pain points. So we covered deployment, the customer and the technical part. Was there a reason you did not use Docker containers?
[~00:21:00] Ali12hamdan: No. Last week we were in a hurry, so we did not set it up as containers; it would be much easier. We usually work with containers, we just did not do it at that time.
[~00:21:00] Customer: That is fine. Do you use an LLM to code or set up, or do you do it by hand?
[~00:21:00] Ali12hamdan: We use LLMs, yes.
[~00:21:00] Customer: Which harness do you use, and what for?
[~00:21:00] Ali12hamdan: I use Codex. I think my teammate also uses Codex.
[~00:21:00] Customer: Then you should be able to tell it to set up a Docker container for this project and let it figure it out. I am also not very good at DevOps; I am forced to do it. But I was able to tell an assistant to set up a lab of virtual machines and test things on them, and it did it. I am not saying you need VMs; it is an example. Containers are quite common, so if you ask Codex to find a way to run this in Docker and version it correctly, it should solve it, and next time you do not look for paths, you just run Docker Compose up and it works.
[~00:23:00] Ali12hamdan: Understood. There are a few smaller things; I am not sure how important they are, but let me lay them out. In the issues we have work on controlling what goes to the model and what comes back. A plugin can add specific text or commands to change the message before it goes to the model, and change the reply. It is not finalized yet; part of it works now. We can also add or rearrange our own rules, but that needs some rewriting. It is a small Python plugin: add it to the configuration and choose when it runs.
[~00:24:00] Customer: What is the interface for your system? It is written in Python, right?
[~00:24:00] Ali12hamdan: Yes.
[~00:24:00] Customer: In the configuration you specify which plugins it runs. Do you just import them with a Python import, or do you do some other magic?
[~00:25:00] Ali12hamdan: You run it in the terminal. One second.
[~00:25:00] Customer: Can I see how plugins are added to the processing pipeline? Is there code that does it?
[~00:25:00] Ali12hamdan: There is code. Let me open that side of it. You cannot see the other window? Give me a second.
[~00:26:00] Customer: I see your editor, Visual Studio Code.
[~00:26:00] Ali12hamdan: We have a plugin JSON file where you can add whatever plugin you want.
[~00:27:00] Customer: Could you show me the thing that actually does the imports: the function that reads the plugin JSON and pulls the plugins in? I am asking so I understand the architecture, how you bring the code into where it runs. That class holds the functions that get called; that is the plugin itself. What about the thing that runs the plugin?
[~00:28:00] Ali12hamdan: Hold on. It is in the gateway, not here; I have to open it somewhere else. [unclear]
[~00:30:00] Ali12hamdan: It should be in the execution part. This should be it. Can you see it?
[~00:30:00] Customer: Yes. It is like a hook: I see the plugin failure handling, you run the plugin and check the instance. I still do not see where it loads, and why you need JSON to load it. That is okay.
[~00:31:00] Ali12hamdan: That file was only for the demo.
[~00:31:00] Customer: I see. I am not sure whether I asked your team or another team this, but as a DevOps customer I would like to know why I would use your code and not just write my own. What do you do that is special, that I could not achieve in a couple of hours with Claude Code or something else?
[~00:32:00] Ali12hamdan: Understood. For now, there is no benefit in switching to our solution. Once we refine it enough, possibly over several iterations, it should be plug and play: you can write your own code, but you want to hand that obligation to something else so you can focus on other things. Our goal is to make it plug and play, so you do not have to work on that part and just use it.
[~00:33:00] Customer: I also want to point out: if I were a DevOps person forced to write some plugins in Python, and I addressed the problem head-on without anything complicated, I would have a bunch of functions, and a main function that calls this one, this one and this one. I would keep updating those functions and the list would grow. Whenever I needed to change my "gateway", I would stop it, add another function to the main, and it would process it.
[~00:34:00] Customer: With a lot of plugins, and more complicated plugins, that becomes very unmanageable, and that is what I have seen people do: they put things together haphazardly, and it is fine and even clear at the beginning, but it gets unruly later. Your solution needs to be something you can sell to the person who does it head-on, and it has to be better. Right now what I see is a more complicated way of calling functions: you wrap them in callbacks.
[~00:35:00] Customer: You need to address this. When you talk to a customer, say why you did this and why it is better than putting all the functions together and calling them from your main, changing it every time. Thinking about that answer while you build it will help you think about the architecture.
[~00:36:00] Ali12hamdan: I have a question. When you say you want to add a plugin, where should you add it from, and what do you have it as? Should there be one place with all the plugins? Can you walk me through how you would like to add a plugin?
[~00:36:00] Customer: Ideally I would have a repository with a bunch of different plugins. When I write a plugin, I focus only on its interface. I do not need to think about how messages travel. If I want to integrate Prometheus, I look up the Prometheus library, wrap it in my plugin, go to the gateway, tell it to load that plugin, and it works.
[~00:37:00] Customer: And it tells me if the plugin failed, or how it performs, or that it is not being used, so I do not miss something. It gives me information. That is what I would expect from such a product.
[~00:38:00] Customer: I do not need to think about how the message is received, how it is processed, what other plugins are running and how it is sent to the cloud provider. Maybe I have another plugin that routes to different providers based on the text, or reroutes to another provider when I run out of credit on one. I would write a plugin that checks the remaining credit and makes the decision, and I do not want to think about everything else while working on that one piece of functionality.
[~00:39:00] Ali12hamdan: I understand.
[~00:39:00] Customer: I agree this is quite challenging to do nicely, and it pushes you quite a bit. I do not expect a perfect solution, but I expect a solution you can show and defend: why you took this way and not another.
[~00:39:00] Customer: Do you have any other questions for me?
[~00:40:00] Ali12hamdan: About the plugins: is it okay for now for it to keep working in the terminal?
[~00:40:00] Customer: Yes, it is fine in the terminal.
[~00:40:00] Ali12hamdan: I do not have any other questions.
[~00:40:00] Customer: So what are you planning for next week?
[~00:40:00] Ali12hamdan: I have to discuss it with the team first. At least: make it easier to add plugins, maybe revise our architecture to see whether there is a simpler way to add and manage plugins.
[~00:41:00] Customer: And the container, right? Docker Compose.
[~00:41:00] Ali12hamdan: Yes. We will also look for alternative solutions. Mainly, make it possible to add plugins that we did not write, from other people, so it works more fluidly; the Docker work; and maybe refine working with the terminal itself, with easier choices. I think that is it.
[~00:41:00] Customer: Sounds good. Good enough.
[~00:41:00] Ali12hamdan: If we finish early, would you like to meet before next Saturday? I would of course contact you ahead of time.
[~00:42:00] Customer: Let us stick to Saturday; it is really hard for me to change. It is easier for me to set the time and keep it, and if we cannot make it, we meet the next week. It is hard to jump from one thing to another.
[~00:42:00] Customer: But you can contact me with any questions. Feel free to use that channel: ask me, show me things, record a demo and put it there, ask about the Docker container or anything. I can respond asynchronously, no problem.
[~00:42:00] Customer: For meetings, structure is good. They serve several purposes; one is for you to practise presenting to a customer and to find a structure for working with one. Next semester you will work with an actual company, with less control over what customers say or do, and it will be up to you and your team to make it work and learn from it. Right now it is a safe environment where I can give you feedback and you can correct.
[~00:43:00] Ali12hamdan: All good.
[~00:44:00] Customer: Thank you for your presentation. For the next meeting, think about what you are going to show, practise it, and target a DevOps person who knows what is going on: address that person's pain points in managing this system.
[~00:44:00] Ali12hamdan: Understood. Thank you for your time and for these insights.
[~00:44:00] Customer: You are welcome. In about an hour I will send the transcript and the recording.
[~00:45:00] Customer: Thank you very much, and see you next week.
[~00:45:00] Ali12hamdan: See you next week. Bye.
