from pomegranate import *
B = DiscreteDistribution({'True': 0.001, 'False': 0.999})
E = DiscreteDistribution({'True': 0.002, 'False': 0.998})
A = ConditionalProbabilityTable(
    [['True', 'True', 'True', 0.95],
     ['True', 'True', 'False', 0.05],
     ['True', 'False', 'True', 0.94],
     ['True', 'False', 'False', 0.06],
     ['False', 'True', 'True', 0.29],
     ['False', 'True', 'False', 0.71],
     ['False', 'False', 'True', 0.001],
     ['False', 'False', 'False', 0.999]], [B, E])

J = ConditionalProbabilityTable(
    [['True', 'True', 0.90],
     ['True', 'False', 0.10],
     ['False', 'True', 0.05],
     ['False', 'False', 0.95]], [A] )

M = ConditionalProbabilityTable(
    [['True', 'True', 0.70],
     ['True', 'False', 0.30],
     ['False', 'True', 0.01],
     ['False', 'False', 0.99]], [A])

s1 = State(B, name = "B")
s2 = State(E, name = 'E')
s3 = State(A, name = 'A')
s4 = State(J, name = "J")
s5 = State(M, name = "M")

model = BayesianNetwork("Burglary")
model.add_states(s1, s2, s3, s4, s5)
model.add_transition(s1, s3)
model.add_transition(s2, s3)
model.add_transition(s3, s4)
model.add_transition(s3, s5)

model.bake()
#P(A)
p_a = model.predict_proba({})[2].parameters[0]['True']
print(model.predict_proba({}))
print('P(Alarm) = ')
print(p_a)
print()

p_jM = model.probability(['True', 'True', 'True', 'True', 'False']) + \
    model.probability(['True', 'True', 'False', 'True', 'False']) + \
    model.probability(['True', 'False', 'True', 'True', 'False']) + \
    model.probability(['True', 'False', 'False', 'True', 'False']) + \
    model.probability(['False', 'True', 'True', 'True', 'False']) + \
    model.probability(['False', 'True', 'False', 'True', 'False']) + \
    model.probability(['False', 'False', 'True', 'True', 'False']) + \
    model.probability(['False', 'False', 'False', 'True', 'False'])
print('P(J&&~M) = ')
print(p_jM)
print()

p_ajM = model.probability(['True', 'True', 'True', 'True', 'False']) + \
    model.probability(['True', 'False', 'True', 'True', 'False']) + \
    model.probability(['False', 'True', 'True', 'True', 'False']) + \
    model.probability(['False', 'False', 'True', 'True', 'False'])
p_a_jM =  p_ajM / p_jM
print('P(A|J&&~M) = ')
print(p_a_jM)
print()

p_b_a = model.predict_proba({'A': 'True'})[0].parameters[0]['True']
print(model.predict_proba({'A': 'True'}))
print('P(B|A) = ')
print(p_b_a)
print()

p_bjM = model.probability(['True', 'True', 'True', 'True', 'False']) + \
    model.probability(['True', 'True', 'False', 'True', 'False']) + \
    model.probability(['True', 'False', 'True', 'True', 'False']) + \
    model.probability(['True', 'False', 'False', 'True', 'False']) 
p_b_jM = p_bjM / p_jM
print('P(B|J&&~M) = ')
print(p_b_jM) 
print()

p_B_jM = 1 - p_b_jM 
p_BjM = p_B_jM * p_jM
p_B = 1- model.predict_proba({})[0].parameters[0]['True']
p_jM_B = p_BjM / p_B
print('P(J&&~M|~B) = ')
print(p_jM_B)
