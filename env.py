# Create the environment
env = make("llm_20_questions", debug=True)

# Reset the environment for a new episode
env.reset()

# Run an episode with the agent function directly
env.run([agent, agent, agent, agent])

# Render the environment to visualize the game
env.render(mode="ipython", width=800, height=700)
