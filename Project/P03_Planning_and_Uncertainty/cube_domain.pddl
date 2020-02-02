(define (domain Cube)
    (:requirements :strips :equality :typing)
    (:types P colour)
    (:predicates (is ?x - P ?y - colour)
                 (state ?p11 - colour ))

(:action U
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action U_
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action D
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action D_
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action F
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action F_
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action B
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action B_
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action R
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action R_
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action L
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action L_
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)

(:action addState
                :parameters (?t - num ?x - loc ?y - loc)
                :precondition (and (at ?t ?x) (adjacent ?x ?y)
                                   (at B ?y))
                :effect (and (at B ?x) (at ?t ?y)
                             (not (at ?t ?x)) (not (at B ?y)) )
)
)