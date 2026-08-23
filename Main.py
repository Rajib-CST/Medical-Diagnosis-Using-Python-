from pathlib import Path

from Greetings import Greetings
diseases_list = []
diseases_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}

BASE_DIR = Path(__file__).resolve().parent

#loads the knowledge from .txt files into variables to allow the code to use it
def preprocess():
    global diseases_list, diseases_symptoms, symptom_map, d_desc_map, d_treatment_map

    diseases_list.clear()
    diseases_symptoms.clear()
    symptom_map.clear()
    d_desc_map.clear()
    d_treatment_map.clear()

    diseases_file = BASE_DIR / "diseases.txt"
    diseases_list.extend(
        disease.strip()
        for disease in diseases_file.read_text(encoding="utf-8").splitlines()
        if disease.strip()
    )

    for disease in diseases_list:
        symptoms_file = BASE_DIR / "Disease symptoms" / f"{disease}.txt"
        s_list = [
            symptom.strip()
            for symptom in symptoms_file.read_text(encoding="utf-8").splitlines()
        ]
        diseases_symptoms.append(s_list)
        symptom_map[str(s_list)] = disease

        description_file = BASE_DIR / "Disease descriptions" / f"{disease}.txt"
        d_desc_map[disease] = description_file.read_text(encoding="utf-8").strip()

        treatment_file = BASE_DIR / "Disease treatments" / f"{disease}.txt"
        d_treatment_map[disease] = treatment_file.read_text(encoding="utf-8").strip()


def identify_disease(*arguments):
    symptom_list = []
    for symptom in arguments:
        symptom_list.append(symptom)

    return symptom_map[str(symptom_list)]


def get_details(disease):
    return d_desc_map[disease]


def get_treatments(disease):
    return d_treatment_map[disease]


def if_not_matched(disease):
    print("")
    id_disease = disease
    disease_details = get_details(id_disease)
    treatments = get_treatments(id_disease)
    print("")
    print("The most probable disease that you have is %s\n" % (id_disease))
    print("A short description of the disease is given below :\n")
    print(disease_details + "\n")
    print(
        "The common medications and procedures suggested by other real doctors are: \n"
    )
    print(treatments + "\n")

#driver function
if __name__ == "__main__":
    preprocess()
    #creating class object
    engine = Greetings(symptom_map, if_not_matched, get_treatments, get_details)
    #loop to keep running the code until user says no when asked for another diagnosis
    while 1:
        engine.reset()
        engine.run()
        print("Would you like to diagnose some other symptoms?\n Reply yes or no")
        if input() == "no":
            exit()