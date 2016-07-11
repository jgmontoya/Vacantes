import requests
from bs4 import BeautifulSoup


def course_info(data, soup):
    data_index = [0, 1, 4, 7, 11, 12]
    course_data_list = []
    info_course = ["nrc", "sigla", "seccion",
                   "nombre", "cantidad_total", "cantidad_dis"]
    course_data_dict = {}
    count = 0
    try:
        busqueda = soup.find('tr', {"class": "resultadosRowPar"})
        for info in busqueda:
            pass
    except TypeError:
        print("Algún(os) de los nrcs es(son) incorrectos")
        return
    for info in busqueda:
        try:
            text = info.get_text()
            if count in data_index:
                course_data_list.append(text)
            count += 1
        except AttributeError:
            pass


    tuples = (list(zip(info_course, course_data_list)))
    for tuple in tuples:
        course_data_dict[tuple[0]] = tuple[1]
    data.append(course_data_dict)


def vacancies_finder(data, final_data):
    for course in data:
        data_index = [6, 7, 8]
        course_data_list = []
        new_r = requests.get('http://buscacursos.uc.cl/informacionVacReserva.ajax.php?nrc=' + str(course["nrc"]) + '&termcode=2016-2&cantidad_dis=' + str(course["cantidad_dis"]) + '&cantidad_min=' + str(
            course["cantidad_total"]) + '&cantidad_ocu=' + str(int(course["cantidad_total"]) - int(course["cantidad_dis"])) + '&nombre=' + str(course["nombre"]) + '&sigla=' + str(course["sigla"]) + '&seccion=' + str(course["seccion"]))
        new_soup = BeautifulSoup(new_r.text, 'html.parser')
        names = []
        final = []
        course_names = new_soup.findAll(
            'td', {"style": "font-size:13px;text-align:left; white-space:normal;word-wrap:break-word;max-width:150px;"})
        for name in course_names:
            names.append(name.get_text().strip())
        vacancies_info = new_soup.findAll('td', {"style" : "font-size:13px;text-align:center;"})
        largo = (len(vacancies_info) - 3)
        vacancies = vacancies_info[3:]
        vacancies
        cont = 0
        name_cont = 0
        new = [names[name_cont]]
        for vac in vacancies:
            new.append(vac.get_text().strip())
            if (int(cont+1) % 3) == 0:
                final.append(new)
                name_cont += 1
                if cont + 1 < largo:
                    new = [names[name_cont]]
            cont += 1
        final_data.append({course["nombre"]: final})

def show_info(final_data):
    for course in final_data:
        for key in course:
            print("Curso: {0} \n ".format(key))
            print("#######################################################")
            for values in course[key]:
                print("Escuela: {0}, \n Ofrecidas = {1}, Ocupadas = {2}, Disponibles = {3}".format(
                values[0], values[1], values[2], values[3]))
            print("####################################################### \n")




while True:

    nrc = input("Ingrese nrc separado por espacio o 'q' para salir: ")
    print("\n")
    if nrc == "q":
        print("bye")
        break
    else:
        try:
            nrcs = nrc.split(" ")
            for i in nrcs:
                int(i)
        except ValueError:
            continue

    data = []
    final_data = []
    for nrc in nrcs:
        r = requests.get(
            "http://buscacursos.uc.cl/?cxml_semestre=2016-2&cxml_sigla=&cxml_nrc=" + nrc + "&cxml_nombre=&cxml_categoria=TODOS&cxml_profesor=&cxml_campus=&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS#resultados")
        soup = BeautifulSoup(r.text, 'html.parser')
        course_info(data, soup)
    vacancies_finder(data, final_data)
    show_info(final_data)
