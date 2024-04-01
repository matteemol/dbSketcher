initUML = """@startuml

left to right direction
skinparam roundcorner 15
skinparam shadowing true
skinparam handwritten false
skinparam class {
    BackgroundColor white
    ArrowColor #2688d4
    BorderColor #2688d4
}

!define table(x) entity x << (T, LightSkyBlue) >>
!define primary_key(x) <b><color:#b8861b><&key></color> x</b>
!define foreign_key(x) <color:#aaaaaa><&key></color> <u>x</u>
!define column(x) <color:#efefef><&media-record></color> x
!define column_fk(x) <color:#efefef><&media-record></color> <u>x</u>

"""

endUML = """
@enduml"""

fkSQL = """
    ON UPDATE SET NULL
    ON DELETE SET NULL"""