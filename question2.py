# imports libraries
import streamlit as st
import constraint
import pandas as pd
import math
import matplotlib.pyplot as plt

st.title("Question 2: Vaccine Distribution Modelling")
st.markdown("The main task is to assign the right vaccine types and amounts to the vaccination centres. Formulate the problem as Constraint Satisfaction Problem.")
st.markdown("We decide to give vaccination priority to people over 60 years old. After that, we will assign vaccines for ages 35 to 60 years old. And lastly, people under 35 years old.")

# creates a list to store number of centres for each state
lst = [[20, 15, 10, 21, 5, 5000], 
       [30, 16, 15, 10, 2, 10000], 
       [22, 15, 11, 12, 3, 7500], 
       [16, 16, 16, 15, 1, 8500], 
       [19, 10, 20, 15, 1, 9500]]

state = [[1, 5000], [2, 10000], [3, 7500], [4, 8500], [5, 9500]]
state_pop = [[115900, 434890, 15000], [100450, 378860, 35234], [223400, 643320, 22318], [269300, 859900, 23893], [221100, 450500, 19284]]

for i in range(len(lst)):
    rental_lst = []
    min_list = []
    solution_found = []

    # creates problem object
    problem = constraint.Problem()

    # defines centre types as variable and number of centres in each state as their respective intervals
    # adds variables into problem
    problem.addVariable("CR1", range(lst[i][0] + 1))  
    problem.addVariable("CR2", range(lst[i][1] + 1))  
    problem.addVariable("CR3", range(lst[i][2] + 1))
    problem.addVariable("CR4", range(lst[i][3] + 1))
    problem.addVariable("CR5", range(lst[i][4] + 1))

    # the sum of vaccines in each centre have to equal to the max vaccine in each state in order to finish vaccine in a fastest way
    def state_max(a, b, c, d, e):  
        if (a*200 + b*500 + c*1000 + d*2500 + e*4000) == lst[i][5]:
            return True

    # adds constraint into problem
    problem.addConstraint(state_max,["CR1", "CR2", "CR3", "CR4", "CR5"])

    min_rental = 99999999 # initializes minimum rental for comparison purpose
    solution_found2 = {}  # creates an empty dictionary to store results
    solutions = problem.getSolutions() # gets solution from python-constraint package

    # gets the minimum rental
    for s in solutions:
        current_rental = s["CR1"]*100 + s["CR2"]*250 + s["CR3"]*500 + s["CR4"]*800 + s["CR5"]*1200
        rental_lst.append(current_rental)
        if current_rental < min_rental:
            min_rental = current_rental
    
    # gets the index of minimum rental in the list
    for idx, rent in enumerate(rental_lst):
        if rent == min_rental:
            min_list.append(idx)
    
    # gets the solution which having the minimum rental using the index got from above
    for x in min_list:
        solution_found2 = solutions[x]
        solution_found2 = dict(sorted(solution_found2.items()))
        solution_found.append(solution_found2)

    # prints results
    st.markdown("""---""")
    subheader = "State {}".format(i + 1)
    st.subheader(subheader)

    st.write("Maximum vaccination capacity per day in this state is", state[i][1])

    st.write("Total number of ways to rent centre: {}".format(len(solutions)))
    st.write("Total number of ways having minimum rental: {}".format(len(solution_found)))
    min_rental_str = "Minimum Rental: RM{}".format(min_rental)
    st.info(min_rental_str)

    st.markdown("**Ways to Rent Centre in Minimum Rental:**")
    
    df = pd.DataFrame(solution_found, index = pd.Index(list(range(1, len(solution_found) + 1)), name = "Way"))
    df.columns.name = df.index.name
    df.index.name = None
    st.write(df.to_html(), unsafe_allow_html = True)

    st.write("#")
    fig, ax = plt.subplots(figsize = (7, 3))

    plt.plot(rental_lst)
    ax.set_xlabel("Number of Ways")
    ax.set_ylabel("Rental (RM)")
    ax.set_title("Rental over Number of Ways")
    st.pyplot(fig)

    st.write("#")
    st.write("Population of state:", sum(state_pop[i]))
    
    st.markdown("**Days to Assign Vaccines:**")
    df2 = pd.DataFrame()
    df2["Age"] = ["< 35", "35 to 60", "> 60"]
    df2["Population"] = state_pop[i]
    df2["Vaccine Type"] = ["VacA", "VacB", "VacC"]
    
    vacA = math.ceil(state_pop[i][0] / state[i][1])
    vacB = math.ceil(state_pop[i][1] / state[i][1])
    vacC = math.ceil(state_pop[i][2] / state[i][1])
    
    df2["Number of Days"] = [vacA, vacB, vacC]
    
    styler = df2.style.hide_index()
    st.write(styler.to_html(), unsafe_allow_html = True)
    st.write("#")
    
    total = vacA + vacB + vacC
    st.write("\nTotal number of days to finish all vaccines:", total, "days")

    
