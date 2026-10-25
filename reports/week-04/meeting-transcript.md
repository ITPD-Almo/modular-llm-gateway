# Week 4 meeting transcript

- **Date:** 2026-10-23.
- **Participants:** Mohammed-Nour, Ali12hamdan, atkond2point0 and Customer, as identified in the supplied transcript.
- **Source:** the locally supplied English transcript, cleaned for readability; false starts and repeated acknowledgments are reduced without changing substantive meaning.
- **Sharing confirmation:** the team owner confirmed on 2026-10-25 that the recording and transcript may be shared; the separate permission questions and answers are not captured in the source.
- **Time markers:** approximate elapsed minutes, shown as `[~HH:MM:00]`; exact recording timecodes and the recording link remain private.

[~00:00:00] Mohammed-Nour: Last week we started the first gateway iteration, defined use cases and ran tests for the pipeline.
[~00:00:00] Customer: Can you show me how the working product works?
[~00:01:00] Customer: Please move the terminal higher because part of it is obscured on my screen.
[~00:02:00] Customer: I can see it now; please continue.
[~00:02:00] Mohammed-Nour: I want to check the installation.
[~00:03:00] Customer: Think aloud so the recording shows what you are trying to do.
[~00:03:00] Customer: Something is not working.
[~00:03:00] Mohammed-Nour: I am trying to install the packages on this laptop; we tested them on another laptop.
[~00:03:00] Mohammed-Nour: There is a problem with my local pip installation.
[~00:04:00] Customer: With Python you should use a virtual environment or environment manager.
[~00:04:00] Customer: Something is not right with the installation steps and copying the environment example.
[~00:04:00] Mohammed-Nour: Ali12hamdan, could you try it on your side?
[~00:05:00] Customer: Let us assume it is installed; walk me through what you would do with it.
[~00:05:00] Mohammed-Nour: We show the configuration and start the metadata and uppercase plugins, then use curl to inspect the plugin trace.
[~00:05:00] Mohammed-Nour: We can reverse the order, restart and send the request again, or remove uppercase and get a lower-case fake reply.
[~00:06:00] Customer: What is your approach to the architecture?
[~00:06:00] Customer: If I write another plugin, how does it enter the list of plugins?
[~00:06:00] Mohammed-Nour: Do you mean adding a new plugin?
[~00:06:00] Customer: Yes; can you hear me?
[~00:06:00] Mohammed-Nour: I could not hear the question clearly; please repeat it.
[~00:07:00] Customer: I wrote a Python file; what is the process that makes it execute as a plugin in your system?
[~00:08:00] Mohammed-Nour: First we write the plugin function and add it here so it can be called.
[~00:08:00] Mohammed-Nour: This main file represents our gateway; [inaudible] call the plugin from the project.
[~00:08:00] Customer: What exactly must I update to install the plugin in your system?
[~00:08:00] Mohammed-Nour: We use Python and need to configure it correctly.
[~00:09:00] Customer: Walk me through what I add after writing the plugin.
[~00:09:00] Mohammed-Nour: We install requirements.txt, which includes the libraries, then move forward.
[~00:09:00] Customer: I have lost the shared screen.
[~00:10:00] Customer: Please share it again and write a simple plugin with me.
[~00:10:00] Customer: Delete the incoming content and put only A letters in its place; replace the LLM response with B letters.
[~00:10:00] Mohammed-Nour: Do you mean removing A letters from the response?
[~00:11:00] Customer: No; ignore the incoming content and replace all of it with four A letters.
[~00:11:00] Customer: I want to understand the process of adding any plugin, starting with the simplest example.
[~00:11:00] Mohammed-Nour: Before adding it, I will show the existing uppercase plugin.
[~00:12:00] Customer: I still cannot see the shared screen.
[~00:12:00] Mohammed-Nour: Here is the gateway and its two plugins; the first checks the request and uppercases it.
[~00:12:00] Customer: I define plugins in code and update this class to add another one?
[~00:12:00] Mohammed-Nour: Yes; I thought I was already sharing that screen.
[~00:13:00] Customer: I saw it but had not understood that this was the process.
[~00:13:00] Mohammed-Nour: Here is the project configuration and the fake provider for test messages.
[~00:13:00] Customer: Can I see a plugin example?
[~00:13:00] Mohammed-Nour: The uppercase plugin defines request processing, takes the message and also defines response processing.
[~00:13:00] Customer: There are process_request and process_response functions which the gateway calls.
[~00:14:00] Customer: I add my plugin to the system in the desired order?
[~00:14:00] Mohammed-Nour: Yes.
[~00:14:00] Customer: How is this different from writing a Python program which calls functions one after another?
[~00:14:00] Mohammed-Nour: It is not very different in the final result.
[~00:15:00] Mohammed-Nour: We are organizing milestones, issues, shared work, reviews, pipelines and tests.
[~00:15:00] Customer: Thank you for the demonstration; please write documentation so another developer can install and run it.
[~00:15:00] Customer: Think about how it improves a developer's experience.
[~00:15:00] Mohammed-Nour: We started implementation last week and intend to go deeper into requirements, tests and documentation this week.
[~00:16:00] Mohammed-Nour: Ali12hamdan and I had been concentrating on documentation and reports while another teammate worked on implementation.
[~00:16:00] Mohammed-Nour: We intend to show better documented and checked results next time.
[~00:16:00] Customer: Do you have questions for me?
[~00:16:00] Mohammed-Nour: [redacted], do you have a question?
[~00:16:00] Ali12hamdan: The plugin process still needs manual configuration; automatic discovery is a possible future improvement.
[~00:17:00] Ali12hamdan: It is not currently something a non-developer can do without that setup.
[~00:17:00] Customer: That is fine; do you have any questions?
[~00:17:00] Mohammed-Nour: How many plugins should we add?
[~00:17:00] Customer: The individual plugins are examples; I am more interested in a system in which I can add and manage my own plugins.
[~00:18:00] Mohammed-Nour: Should adding them be easier for developers or for non-developers?
[~00:18:00] Customer: Developers and DevOps operators are the users.
[~00:18:00] Customer: A good outcome would be documentation sufficient for an LLM to produce a compatible plugin.
[~00:18:00] Customer: The product is a plugin-management system for an LLM gateway and must offer value beyond manually joining functions.
[~00:19:00] Customer: A custom set of generated functions can become a system nobody else understands or can support.
[~00:19:00] Customer: Another DevOps operator should be able to take it over and support it.
[~00:19:00] Mohammed-Nour: Should the system check and handle a plugin timeout?
[~00:19:00] Customer: Yes; the system should manage even badly written plugins.
[~00:20:00] Customer: If a plugin sleeps for minutes or otherwise times out, the system should keep working, stop executing that plugin, identify that something is wrong and log it somehow.
[~00:20:00] Customer: It should handle those plugins in the gateway's request and response workflow; logging is one example of useful supporting behavior.
[~00:21:00] Customer: Does that make sense; can you hear me?
[~00:21:00] Ali12hamdan: [redacted: personal connectivity details].
[~00:21:00] Customer: [redacted: personal connectivity details].
[~00:21:00] Ali12hamdan: Can we change the meeting time?
[~00:22:00] Customer: [redacted: personal scheduling and time-zone details].
[~00:22:00] Ali12hamdan: We would need to discuss a change with the other teams too.
[~00:23:00] Customer: This is the most stable meeting slot I can offer.
[~00:23:00] Ali12hamdan: Understood; thank you for explaining.
[~00:23:00] Customer: You do not need to wait for the meeting to ask questions; asynchronous questions are welcome.
[~00:23:00] Customer: If you have something to show, one presenter can show it; I am flexible about the presentation.
[~00:24:00] Customer: I want to see project progress and a vision beyond one iteration.
[~00:24:00] Customer: Show that you know where the product is going and what you are building.
[~00:25:00] Customer: Plan across several weeks, show whether you hit your goals, track execution and adjust the plan when needed.
[~00:26:00] Customer: Practicing those planning and tracking skills matters for the course.
[~00:26:00] Ali12hamdan: Understood; we will ask further questions asynchronously.
[~00:26:00] Customer: Please do.
[~00:26:00] Ali12hamdan: Does anyone have another question?
[~00:26:00] Mohammed-Nour: No more questions from me; thank you.
[~00:26:00] Customer: Thank you for joining.
[~00:26:00] Mohammed-Nour: Have a good day.
[~00:26:00] atkond2point0: Thank you.
[~00:26:00] Customer: Goodbye.
