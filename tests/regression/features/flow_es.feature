# language: es
@flow
Característica: Pasos condicionales en español

  Antecedentes:
    Dado que tengo un cliente Judo API
    Y la URL base es "__BASE__"

  Escenario: si / en caso contrario
    Cuando hago una petición GET a "/status?code=404"
    Y si el estado de la respuesta es 404 entonces ejecuto
      """
      Cuando hago una petición POST a "/users" con el cuerpo
        '''
        {"name": "Ana"}
        '''
      Entonces el código de respuesta debe ser 201
      Y establezco la variable "rama" a "si"
      """
    Y en caso contrario ejecuto
      """
      Entonces fallo la prueba con el mensaje "no debe ejecutarse"
      """
    Entonces la variable "rama" debe estar definida

  Escenario: condiciones sobre JSON, variables y entorno
    Cuando hago una petición GET a "/users/1"
    Y si la respuesta "$.age" es mayor que 18 entonces ejecuto
      """
      Y establezco la variable "adulto" a "si"
      """
    Y si la respuesta "$.tags" contiene "b" entonces ejecuto
      """
      Y establezco la variable "tiene_b" a "si"
      """
    Y si la variable "fantasma" no está definida entonces ejecuto
      """
      Y establezco la variable "sin_fantasma" a "si"
      """
    Y si el entorno es "nunca" entonces ejecuto
      """
      Entonces fallo la prueba con el mensaje "no debe ejecutarse"
      """
    Entonces la variable "adulto" debe estar definida
    Y la variable "tiene_b" debe estar definida
    Y la variable "sin_fantasma" debe estar definida

  Escenario: bucles, reintentos y aserciones suaves
    Cuando hago una petición GET a "/users"
    Y para cada elemento en la respuesta "$" ejecuto
      """
      Cuando hago una petición GET a "/echo?id=${item.id}"
      Entonces la respuesta "$.query.id" debe ser "${item.id}"
      """
    Y repito 2 veces
      """
      Cuando hago una petición GET a "/echo?n=${iteration}"
      Entonces la respuesta "$.query.n" debe ser "${iteration}"
      """
    Dado hago una petición GET a "/reset"
    Cuando reintento los siguientes pasos hasta 5 veces con 0.05 segundos de espera
      """
      Cuando hago una petición GET a "/flaky"
      Entonces el código de respuesta debe ser 200
      """
    Entonces verifico todo lo siguiente
      """
      Entonces el código de respuesta debe ser 200
      Y la respuesta debe ser exitosa
      """

  Escenario: saltar el escenario
    Dado que establezco la variable "modo" a "saltar"
    Cuando salto el escenario si la variable "modo" es igual a "saltar"
    Entonces fallo la prueba con el mensaje "un escenario saltado no llega aquí"
