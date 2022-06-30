
(cl:in-package :asdf)

(defsystem "local_pkg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Displacement" :depends-on ("_package_Displacement"))
    (:file "_package_Displacement" :depends-on ("_package"))
    (:file "Displacement" :depends-on ("_package_Displacement"))
    (:file "_package_Displacement" :depends-on ("_package"))
  ))