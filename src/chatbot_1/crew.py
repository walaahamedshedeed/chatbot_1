from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
import hashlib
import time
from chatbot_1.tools.time_tool import TimeTool

# Create a knowledge source
# content = "Users name is Walaa. He is 30 years old and lives in UAE"
# string_source = StringKnowledgeSource(
#     content=content,
# 	metadata={"source":"user_profile"}
# )


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Chatbot1():
	"""Chatbot1 crew"""
	def __init__(self):
        # Add timestamp to make each instance unique
		timestamp = str(time.time())
		self.string_source = TextFileKnowledgeSource(
            file_path=["user_preference.txt"],
            metadata={
                "source": "user_data",
                "instance_id": hashlib.md5(timestamp.encode()).hexdigest()
            }
        )

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'



	# # If you would like to add tools to your agents, you can learn more about it here:
	# # https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def assistant(self) -> Agent:
		return Agent(
			config=self.agents_config['assistant'],
			verbose=True,
			allow_delegation=False,
			tools=[TimeTool()]
		)
	


	# @agent
	# def reporting_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reporting_analyst'],
	# 		verbose=True
	# 	)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def assistant_task(self) -> Task:
		return Task(
			config=self.tasks_config['assistant_task'],
			agent=self.assistant()
		)

	# @task
	# def reporting_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reporting_task'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the Chatbot1 crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			knowledge_sources=[self.string_source],
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
