'use strict'

let router = require('express').Router();
let ClockCtrl = require('../controllers/real_time');

router.get('/', ClockCtrl.get_time);

module.exports = router;