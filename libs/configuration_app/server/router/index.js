'use strict'

let router = require('express').Router();
let ViewCtrl = require('../controllers/view');

router.get('/', ViewCtrl.dashboard);
router.get('/add/cycle', ViewCtrl.add_cycle);
router.get('/edit/cycle/:day/:ID', ViewCtrl.edit_cycle);
router.get('/change_system_hour', ViewCtrl.change_system_hour);
router.get('/system_test', ViewCtrl.system_test);

module.exports = router;