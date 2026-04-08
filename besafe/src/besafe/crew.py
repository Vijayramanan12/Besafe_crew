from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from crewai.project import CrewBase, agent, crew, task, tool
from crewai.agents.agent_builder.base_agent import BaseAgent
from datetime import date
from besafe.tools.custom_tool import MyCustomTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Besafe():
    """Besafe crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def extracters(self) -> Agent:
        return Agent(
            config=self.agents_config['extracters'], # type: ignore[index]
            tools=[MyCustomTool()],
            verbose=True
        )

    @tool
    def fetch_code(self) -> BaseTool:
        return MyCustomTool()

    @agent
    def scanner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scanner_agent'], # type: ignore[index]
            verbose=True
        )
        
    @agent
    def context_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['context_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def risk_scorer(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_scorer'], # type: ignore[index]
            verbose=True
        )
        
    @agent
    def remediation_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['remediation_advisor'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def extracter_task(self) -> Task:
        return Task(
            config=self.tasks_config['extracter_task'], # type: ignore[index]
            inputs={'url': '{url}'}
        )

    @task
    def scanner_task(self) -> Task:
        return Task(
            config=self.tasks_config['scanner_task'], # type: ignore[index]
        )
        
    @task
    def context_task(self) -> Task:
        return Task(
            config=self.tasks_config['context_task'], # type: ignore[index]
        )
        
    @task
    def risk_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_task'], # type: ignore[index]
        )
        
    @task
    def remediation_task(self) -> Task:
        return Task(
            config=self.tasks_config['remediation_task'], # type: ignore[index]
        )
    
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Besafe crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
