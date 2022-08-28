
(cl:in-package :asdf)

(defsystem "semi_final_pkg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "gigacha" :depends-on ("_package_gigacha"))
    (:file "_package_gigacha" :depends-on ("_package"))
  ))