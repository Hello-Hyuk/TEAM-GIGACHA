
(cl:in-package :asdf)

(defsystem "new_gigacha-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Perception" :depends-on ("_package_Perception"))
    (:file "_package_Perception" :depends-on ("_package"))
    (:file "Perception" :depends-on ("_package_Perception"))
    (:file "_package_Perception" :depends-on ("_package"))
  ))