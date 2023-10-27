from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from tkinter import *
from tkinter import ttk

def quantum_circuit(q0,q1,q2):
    # Initialize circuit
    qr = QuantumRegister(3, 'q')
    anc = QuantumRegister(2, 'ancilla')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qr, anc, cr)

    # define initial state / message for single logical qubit
    if(q0):
        qc.x(qr[0])
    if(q1):
        qc.x(qr[1])
    if(q2):
        qc.x(qr[2])

    # attempt correction
    qc.cx(qr[0],anc[0])
    qc.cx(qr[1],anc[0])
    qc.cx(qr[1],anc[1])
    qc.cx(qr[2],anc[1])

    qc.ccx(anc[0],anc[1],qr[1])

    qc.x(anc[1])
    qc.ccx(anc[0],anc[1],qr[0])
    qc.x(anc[1])

    qc.x(anc[0])
    qc.ccx(anc[0],anc[1],qr[2])
    qc.x(anc[0])


    # measure results
    qc.measure([0,1,2],[0,1,2])

    # simulate code
    backend = AerSimulator()
    qc_compiled = transpile(qc, backend)
    job_sim = backend.run(qc_compiled, shots=1024)
    result_sim = job_sim.result()

    # print results
    return result_sim.get_counts(qc_compiled)


root = Tk()
root.title("Quantum Bit Flip Code")
frm = ttk.Frame(root, padding=20)
frm.grid()
q0 = IntVar()
q1 = IntVar()
q2 = IntVar()
output = StringVar()

def quantumize():
    output.set("Quantumizing...")
    results = quantum_circuit(q0.get()==1,q1.get()==1,q2.get()==1)
    output.set("Corrected code is: " + list(results.keys())[0])


ttk.Label(frm, text="Logical Qubit:").grid(column=0, row=0)
ttk.Checkbutton(frm, text="Qubit 0", variable=q0).grid(column=0, row=1)
ttk.Checkbutton(frm, text="Qubit 1", variable=q1).grid(column=1, row=1)
ttk.Checkbutton(frm, text="Qubit 2", variable=q2).grid(column=2, row=1)
ttk.Label(frm, textvariable=output).grid(column=0, row=3, columnspan=3)
ttk.Button(frm, text="Correct my Logical Qubit!", command=quantumize).grid(column=0, row=2, columnspan=3)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=4, columnspan=3)
root.mainloop()
