# language: es
@new
Característica: Pasos nuevos (v1.7.0) en español

  Antecedentes:
    Dado que tengo un cliente Judo API
    Y la URL base es "__BASE__"

  Escenario: Interpolación
    Dado que establezco la variable "quien" a "Ana"
    Cuando hago una petición GET a "/echo?a=${quien}&b=${nada:-por_defecto}"
    Entonces la respuesta "$.query.a" debe ser "Ana"
    Y la respuesta "$.query.b" debe ser "por_defecto"

  Escenario: Headers y seguridad
    Cuando hago una petición GET a "/secure"
    Entonces el header de respuesta "X-Frame-Options" debe ser "DENY"
    Y el header de respuesta "strict-transport-security" debe existir
    Y la respuesta debe incluir headers de seguridad

  Escenario: XML y SOAP
    Cuando hago una petición GET a "/xml"
    Entonces el XML de la respuesta "//user[@id='2']/name" debe ser "Luis"
    Y el XML de la respuesta "//user" debe seleccionar 2 nodos
    Cuando envío una petición SOAP a "/echo" con la acción "urn:es"
      """
      <Envelope/>
      """
    Entonces la respuesta "$.headers.soapaction" debe ser "urn:es"

  Escenario: Configuración HTTP, archivos y SQL
    Dado que establezco el timeout a 10 segundos
    Cuando subo el archivo "data/hello.txt" como "file" a "/upload"
    Entonces la respuesta debe contener el campo "sha256"
    Cuando hago una petición GET a "/download"
    Entonces el SHA-256 de la respuesta debe ser "__SHA__"
    Dado que me conecto a la base de datos "sqlite:///:memory:"
    Y ejecuto el SQL "create table t(x integer)"
    Y ejecuto el SQL "insert into t values (5)"
    Entonces la consulta SQL "select x from t" debe devolver 1 filas
    Cuando consulto "/job" hasta que el estado sea 200 en máximo 5 segundos
