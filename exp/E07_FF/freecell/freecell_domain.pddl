(define (domain freecell)
	(:requirements :strips :equality:typing:universal-preconditions:conditional-effects)
	(:types card cellnum colnum num suit)
	(:predicates  (VALUE ?x - card ?y - num)
				  (CELLSUCCESSOR ?x ?y - cellnum)
				  (COLSUCCESSOR ?x ?y - colnum)
				  (SUCCESSOR ?x ?y - num)
				  (SUIT ?x - card ?y - suit)
				  (CANSTACK ?x ?y - card)
				  (INCELL ?x - card)
				  (HOME ?x - card)
				  (CELLSPACE ?x - cellnum)
				  (COLSPACE ?x - colnum)
				  (BOTTOMCOL ?x - card)
				  (ON ?x ?y - card)
				  (CLEAR ?x - card))
	
	(:action SENDTOHOME
		:parameters (?card ?oldcard - card ?suit - suit ?vcard - num
                ?homecard - card ?vhomecard - num)
		:precondition (and (CLEAR ?card) (ON ?card ?oldcard) (SUIT ?card ?suit) (HOME ?homecard) (SUIT ?homecard ?suit) (VALUE ?card ?vcard) (VALUE ?homecard ?vhomecard) (SUCCESSOR ?vcard ?vhomecard)  )
		:effect (and (not(CLEAR ?card)) (not(ON ?card ?oldcard)) (CLEAR ?oldcard)  (HOME ?card) )
	)

	(:action SENDTOHOME-B
		:parameters (?card - card ?suit - suit  ?vcard - num
                ?homecard - card
                ?vhomecard - num
                ?cols ?ncols - colnum)
		:precondition (and (BOTTOMCOL ?card) (CLEAR ?card) (HOME ?homecard) (SUIT ?card ?suit) (SUIT ?homecard ?suit) (VALUE ?card ?vcard) (VALUE ?homecard ?vhomecard) (SUCCESSOR ?vcard ?vhomecard) (COLSUCCESSOR ?ncols ?cols) (COLSPACE ?cols) )
		:effect (and (not(BOTTOMCOL ?card)) (not(CLEAR ?card)) (HOME ?card) (COLSPACE ?ncols) (not(COLSPACE ?cols)) )
	)

	(:action HOMEFROMFREECELL
		:parameters (?card - card ?suit - suit ?vcard - num
                ?homecard - card ?vhomecard - num
                ?cells ?ncells - cellnum)
		:precondition (and (INCELL ?card) (SUIT ?card ?suit) (HOME ?homecard) (SUIT ?homecard ?suit) (VALUE ?card ?vcard)  (VALUE ?homecard ?vhomecard) (SUCCESSOR ?vcard ?vhomecard) (CELLSUCCESSOR ?ncells ?cells) (CELLSPACE ?cells) )
		:effect (and (not(INCELL ?card)) (HOME ?card) (CELLSPACE ?ncells) (not(CELLSPACE ?cells)) )
	)

	(:action MOVE
       :parameters (?card ?oldcard ?newcard - card)
       :precondition (and (CLEAR ?card) (CLEAR ?newcard) (ON ?card ?oldcard) (CANSTACK ?card ?newcard) )
       :effect (and (not(CLEAR ?newcard)) (ON ?card ?newcard) (CLEAR ?oldcard) (not(ON ?card ?oldcard)) )
	)

	(:action MOVE-B
       :parameters (?card ?newcard - card ?cols ?ncols - colnum)
       :precondition (and (BOTTOMCOL ?card) (CLEAR ?card) (CLEAR ?newcard) (COLSUCCESSOR ?ncols ?cols) (COLSPACE ?cols) (CANSTACK ?card ?newcard) )
       :effect (and (not(BOTTOMCOL ?card)) (not(CLEAR ?newcard)) (ON ?card ?newcard) (COLSPACE ?ncols) (not(COLSPACE ?cols)) )
	)


	(:action SENDTOFREE 
       :parameters (?card ?oldcard - card ?cells ?ncells - cellnum)
       :precondition (and (CLEAR ?card) (ON ?card ?oldcard) (CELLSUCCESSOR ?cells ?ncells) (CELLSPACE ?cells) )
       :effect (and  (INCELL ?card) (not(CLEAR ?card)) (not(ON ?card ?oldcard)) (CLEAR ?oldcard ) (CELLSPACE ?ncells) (not(CELLSPACE ?cells)) )
	)

	(:action SENDTOFREE-B 
       :parameters (?card - card ?cells ?ncells - cellnum ?cols ?ncols - colnum)
       :precondition (and (BOTTOMCOL ?card) (CLEAR ?card) (CELLSUCCESSOR ?cells ?ncells) (CELLSPACE ?cells) (COLSUCCESSOR ?ncols ?cols) (COLSPACE ?cols) )
       :effect (and (INCELL ?card) (not(BOTTOMCOL ?card)) (not(CLEAR ?card)) (CELLSPACE ?ncells) (not(CELLSPACE ?cells)) (COLSPACE ?ncols) (not(COLSPACE ?cols)) )
	)
	
	(:action SENDTONEWCOL
		:parameters (?card ?oldcard - card ?cols ?ncols - colnum)
		:precondition (and (CLEAR ?card) (ON ?card ?oldcard) (COLSUCCESSOR ?cols ?ncols) (COLSPACE ?cols) )
		:effect (and (not(ON ?card ?oldcard)) (CLEAR ?oldcard) (BOTTOMCOL ?card) (COLSPACE ?ncols) (not(COLSPACE ?cols)) )
	)

	(:action colfromfreecell
		:parameters (?card ?newcard -  card ?cells ?ncells - cellnum)
		:precondition (and (INCELL ?card) (CLEAR ?newcard) (CANSTACK ?card ?newcard) (CELLSUCCESSOR ?ncells ?cells) (CELLSPACE ?cells) )
		:effect (and (not(INCELL ?card)) (not(CLEAR ?newcard)) (CLEAR ?card) (ON ?card ?newcard) (CELLSPACE ?ncells) (not(CELLSPACE ?cells)) )
	)

	(:action newcolfromfreecell
		:parameters (?card - card ?cols ?ncols - colnum ?cells ?ncells - cellnum)
		:precondition (and (INCELL ?card) (CELLSUCCESSOR ?ncells ?cells) (CELLSPACE ?cells) (COLSUCCESSOR ?cols ?ncols) (COLSPACE ?cols) )
		:effect (and (not(INCELL ?card)) (BOTTOMCOL ?card) (CLEAR ?card) (CELLSPACE ?ncells) (not(CELLSPACE ?cells)) (COLSPACE ?ncols) (not(COLSPACE ?cols)) )
	)
)
