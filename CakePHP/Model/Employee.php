<?php
App::uses('AppModel', 'Model');
/**
 * Employee Model
 *
 */
class Employee extends AppModel {
	var $validate = array(
		'nazwisko' => array(
			'rule' => 'notBlank',
			'message' => 'Please enter a surname'
		),
		'etat' => array(
			'rule' => 'notBlank',
			'message' => 'Please enter job position'
		),
		'placa_pod' => array(
			'rule' => array('range', 0, 2000),
			'message' => 'Please enter a number between 0 and 2000'
		)
	);
}
