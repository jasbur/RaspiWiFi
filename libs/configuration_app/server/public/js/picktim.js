/**
 * Basic Timepicker component for custom use
 *
 * @author JA Engelbrecht
 *
 * @license MIT <http://opensource.org/licenses/MIT>
 */

(function ( $ ) {
'use strict';

    var pluginName = 'picktim';

    function Plugin( element, options ) {
        var thisRef = this;
        this.MODES = {
            h12: 'h12',
            h24: 'h24'
        };
        this.ORIENTATIONS = {
            topLeft: 'topLeft',
            topRight: 'topRight',
            bottomLeft: 'bottomLeft',
            bottomRight: 'bottomRight',
            leftTop: 'leftTop',
            leftBottom: 'leftBottom',
            rightTop: 'rightTop',
            rightBottom: 'rightBottom'
        };
        this.element = element[0];
        this.$element = $(this.element);
    this.settings = $.extend({
        // Defaults
        backgroundColor: "#EEE",
        borderColor: "#DDD",
        textColor: "#333",
        symbolColor: "#333",
        appendTo: 'body',
        mode: this.MODES.h24,
        orientation: this.ORIENTATIONS.bottomLeft,
        defaultValue: '00:00',
        formName: '',
        icons: {
            up: 'fa fa-chevron-up fa-fw',
            down: 'fa fa-chevron-down fa-fw',
            clear: 'fa fa-times fa-fw'
        }
    }, options );
    this.timeouts = {
        iH: 0,
        dH: 1,
        iM: 2,
        dM: 3
    };
    // check and set default value
    if (this.settings.defaultValue === 'now')
    {
        var curTim = new Date();
        this.setDefaultValue(('0' + curTim.getHours()).slice(-2) + ':' + ('0' + curTim.getMinutes()).slice(-2));
    }
    if (!this.validTime(this.settings.defaultValue))
    {
        this.setDefaultValue('00:00');
    }
    this.incrementInterval = 150;
    this.incrementUpCount = 0;
    this.incrementValue = 1;

    // setup structure. Internal elements referenced for easier customization
    this.position = $(this).offset();
    this._name = pluginName;

    this.input = $('<input>');
    this.input.addClass('time-input');
    this.input.attr('id','new_hour');
    this.input.attr('maxlength','5');
    this.input.attr('readonly',true);
    if (this.settings.formName !== '' && this.settings.formName !== null)
    {
        this.input.addClass('form-control');
        this.input.attr('name', this.settings.formName);
    }
    this.input.attr('type', 'text');
    this.$element.append(this.input);
    this.tPopup = $('<div>');
    this.tPopup.addClass('picktim-container');
    if (this.settings.mode === this.MODES.h24)
    {
        this.tPopup.get(0).style.setProperty('--picktim-container-width', '150px');
    }
    else{
        this.tPopup.get(0).style.setProperty('--picktim-container-width', '200px');
    }
    this.setOrientation();
    this.tPopup.hide();
    $(this.settings.appendTo).append(this.tPopup);
    this.cTable = $('<table>');
    this.cTable.addClass('picktim-table');
    this.tPopup.append(this.cTable);
    this.cTable.topRow = $('<tr>');
    this.cTable.midRow = $('<tr>');
    this.cTable.botRow = $('<tr>');
    this.cTable.append(this.cTable.topRow);
    this.cTable.append(this.cTable.midRow);
    this.cTable.append(this.cTable.botRow);
    this.cTable.topRow.c1 = $('<td>'); this.cTable.topRow.c2 = $('<td>');this.cTable.topRow.c3 = $('<td>');this.cTable.topRow.c4 = $('<td>');
    this.cTable.topRow.append(this.cTable.topRow.c1, this.cTable.topRow.c2, this.cTable.topRow.c3, this.cTable.topRow.c4);
    this.cTable.midRow.c1 = $('<td>'); this.cTable.midRow.c2 = $('<td>');this.cTable.midRow.c3 = $('<td>');this.cTable.midRow.c4 = $('<td>');
    this.cTable.midRow.append(this.cTable.midRow.c1, this.cTable.midRow.c2, this.cTable.midRow.c3, this.cTable.midRow.c4);
    this.cTable.botRow.c1 = $('<td>'); this.cTable.botRow.c2 = $('<td>');this.cTable.botRow.c3 = $('<td>');this.cTable.botRow.c4 = $('<td>');
    this.cTable.botRow.append(this.cTable.botRow.c1, this.cTable.botRow.c2, this.cTable.botRow.c3, this.cTable.botRow.c4);
    this.tHours = $('<input>');
    this.tHours.attr('type', 'text');
    this.tHours.addClass('picktim-hour');
    this.tHours.on('change', $.proxy(function () {
     this.updateInput();
    },this));
    this.cTable.midRow.c1.append(this.tHours);
    this.tMins = $('<input>')
    this.tMins.attr('type', 'text');
    this.tMins.addClass('picktim-mins')
    this.tMins.on('change', $.proxy(function () {
     this.updateInput();
    },this));
    this.cTable.midRow.c3.append(this.tMins);
    this.cTable.midRow.c2.text(':');
    this.cTable.midRow.c2.addClass('picktim-separator picktim-symbol');
    this.incHours = $('<i>');
    this.incHours.addClass('picktim-btn picktim-symbol');
    this.incHours.addClass(this.settings.icons.up);
    this.incHours.on('mousedown touchstart', $.proxy(function (e) {
        this.incrementHours();
        this.tHours.addClass('active');
        this.timeouts.iH = setInterval($.proxy(function () {
            this.incrementHours(this.incrementValue);
            if (this.incrementUpCount < 5)
            {
                this.incrementUpCount ++;
            }
            else if (this.incrementUpCount === 5)
            {
                this.incrementValue = 5;
                this.incrementUpCount ++;
            }
        },this), this.incrementInterval);
    },this)).bind('mouseup mouseleave touchend', $.proxy(function () {
        this.tHours.removeClass('active');
        clearInterval(this.timeouts.iH);
        this.incrementUpCount = 0;
        this.incrementValue = 1;
    },this));
    this.cTable.topRow.c1.append(this.incHours);
    this.decHours = $('<i>');
    this.decHours.addClass('picktim-btn picktim-symbol');
    this.decHours.addClass(this.settings.icons.down);
    this.decHours.on('mousedown touchstart', $.proxy(function (e) {
        this.decrementHours();
        this.tHours.addClass('active');
        this.timeouts.dH = setInterval($.proxy(function () {
            this.decrementHours(this.incrementValue);
            if (this.incrementUpCount < 5)
            {
                this.incrementUpCount ++;
            }
            else if (this.incrementUpCount === 5)
            {
                this.incrementValue = 5;
                this.incrementUpCount ++;
            }
        },this), this.incrementInterval);
    },this)).bind('mouseup mouseleave touchend', $.proxy(function () {
        this.tHours.removeClass('active');
        clearInterval(this.timeouts.dH);
        this.incrementUpCount = 0;
        this.incrementValue = 1;
    },this));
    this.cTable.botRow.c1.append(this.decHours);
    this.incMins = $('<i>');
    this.incMins.addClass('picktim-btn picktim-symbol');
    this.incMins.addClass(this.settings.icons.up);
    this.incMins.on('mousedown touchstart', $.proxy(function (e) {
        this.incrementMinutes();
        this.tMins.addClass('active');
        this.timeouts.iM = setInterval($.proxy(function () {
            this.incrementMinutes(this.incrementValue);
            if (this.incrementUpCount < 5)
            {
                this.incrementUpCount ++;
            }
            else if (this.incrementUpCount === 5)
            {
                this.incrementValue = 5;
                this.incrementUpCount ++;
            }
        },this), this.incrementInterval);
    },this)).bind('mouseup mouseleave touchend', $.proxy(function () {
        this.tMins.removeClass('active');
        clearInterval(this.timeouts.iM);
        this.incrementUpCount = 0;
        this.incrementValue = 1;
    },this));
    this.cTable.topRow.c3.append(this.incMins);
    this.decMins = $('<i>');
    this.decMins.addClass('picktim-btn picktim-symbol');
    this.decMins.addClass(this.settings.icons.down);
    this.decMins.on('mousedown touchstart', $.proxy(function (e) {
        this.decrementMinutes();
        this.tMins.addClass('active');
        this.timeouts.dM = setInterval($.proxy(function () {
            this.decrementMinutes(this.incrementValue);
            if (this.incrementUpCount < 5)
            {
                this.incrementUpCount ++;
            }
            else if (this.incrementUpCount === 5)
            {
                this.incrementValue = 5;
                this.incrementUpCount ++;
            }
        },this), this.incrementInterval);
    },this)).bind('mouseup mouseleave touchend', $.proxy(function () {
        this.tMins.removeClass('active');
        clearInterval(this.timeouts.dM);
        this.incrementUpCount = 0;
        this.incrementValue = 1;
    },this));
    this.cTable.botRow.c3.append(this.decMins);
    this.clearBtn = $('<i>')
    this.clearBtn.addClass('picktim-clear');
    this.clearBtn.addClass(this.settings.icons.clear);
    this.$element.append(this.clearBtn);
    this.clearBtn.css({
        color: this.input.css('color')
    });
    this.clearBtn.on('click', $.proxy(function () {
        this.input.val('');
    },this));
    this.ampm = $('<div>');
    if (this.settings.mode === this.MODES.h12)
        this.ampm.addClass('picktim-btn picktim-ampm');
    this.cTable.midRow.c4.append(this.ampm);
    if (this.settings.mode === this.MODES.h24)
    {
        this.ampm.text('');
    }
    else {
        this.ampm.text('AM');
    }
    this.ampm.on('click', $.proxy(function () {
        if (this.ampm.text() == 'AM')
        {
            this.ampm.text('PM');
        }
        else {
            this.ampm.text('AM');
        }
        this.updateInput();
    },this));

    this.input.on('change', $.proxy(function () {
        this.checkTime();
    },this));

    this.tPopup.on('click', function(e){
        e.stopPropagation();
    });

    this.input.click(function(e){
        e.stopPropagation();
        if (!thisRef.tPopup.hasClass('active'))
        {
            thisRef.showPopup();
            if (thisRef.value() === '')
            {
                thisRef.updateInput();
            }
            $('body').one('click', function(){
                thisRef.hidePopup();
            });
        }
    })

    // set colours
    this.cTable.find(".picktim-symbol").css('color', this.settings.symbolColor);
    this.tPopup.css('background-color', this.settings.backgroundColor);
    this.tPopup.css('border-color', this.settings.borderColor);
    this.tPopup.css('color', this.settings.textColor);

    return this;
};

// Set/return the input value
Plugin.prototype.value = function(e)
{
    if (typeof e != 'undefined' && e != null)
    {
        this.input.val(e);
    }
    else {
        return this.input.val();
    }
}

// Show Popup
 Plugin.prototype.showPopup = function(){
     this.setOrientation();
    this.tPopup.show();
    this.tPopup.addClass('active');
}

// Hide Popup
Plugin.prototype.hidePopup = function(){
    this.tPopup.hide();
    this.tPopup.removeClass('active');
}

// Set the popup's position
Plugin.prototype.setOrientation = function(){
    switch (this.settings.orientation)
    {
        case this.ORIENTATIONS.bottomLeft:
        this.tPopup.css({
        top: this.input.offset().top + 10 + this.input.outerHeight(),
        left: this.input.offset().left
        });
        break;
        case this.ORIENTATIONS.bottomRight:

        this.tPopup.css({
        top: this.input.offset().top + 10 + this.input.outerHeight(),
        left: this.input.offset().left + this.input.outerWidth()
        });
        break;
        case this.ORIENTATIONS.topLeft:
        // var pHeight = getComputedStyle(document.body).getPropertyValue("--picktim-container-height");
        this.tPopup.css({
        top: this.input.offset().top - 130,
        left: this.input.offset().left
        });
        break;
        case this.ORIENTATIONS.topRight:
        this.tPopup.css({
        top: this.input.offset().top - 130,
        left: this.input.offset().left + this.input.outerWidth()
        });
        break;
        case this.ORIENTATIONS.leftBottom:
        this.tPopup.css({
        top: this.input.offset().top +  this.input.outerHeight(),
        left: this.input.offset().left - 10 - this.tPopup.outerWidth()
        });
        break;
        case this.ORIENTATIONS.leftTop:
        this.tPopup.css({
            top: this.input.offset().top,
            left: this.input.offset().left - 10 - this.tPopup.outerWidth()
        });
        break;
        case this.ORIENTATIONS.rightBottom:
        this.tPopup.css({
        top: this.input.offset().top + this.input.outerHeight(),
        left: this.input.offset().left + 10 + this.input.outerWidth()
        });
        break;
        case this.ORIENTATIONS.rightTop:
        this.tPopup.css({
            top: this.input.offset().top,
            left: this.input.offset().left + 10 + this.input.outerWidth()
        });
        break;
        default:
        console.log(this.settings.orientation);
        this.tPopup.css({
        top: this.input.offset().top + 10 + this.input.outerHeight(),
        left: this.input.offset().left
        });
        break;
    }
}

// Update the input from popup values
Plugin.prototype.updateInput = function(){
    this.checknums();
    if (this.settings.mode === this.MODES.h24)
    {
        this.input.val(this.tHours.val() + ":" + this.tMins.val());
    }
    else {
        if (this.ampm.text() === 'AM')
        {
            this.input.val(this.tHours.val() + ":" + this.tMins.val());
        }
        else{
            this.input.val((parseInt(this.tHours.val()) + 12) + ":" + this.tMins.val());
        }

    }

}

// Validate popup values
Plugin.prototype.checknums = function(e){
    var h = this.tHours;
    var m = this.tMins;
    var th = parseInt(h.val(), 10);
    var tm = parseInt(m.val(), 10);
    var td = this.settings.defaultValue.split(':');
    var tdh = parseInt(td[0], 10);
    var tdm = parseInt(td[1], 10);
        if (isNaN(th))
        {
            h.val(td[0]);
            h.data['val'] = tdh;
            th = tdh;
        }
        if (h.val() === '')
        {
            h.val(td[0]);
            h.data['val'] = tdh;
        }
        else if (this.settings.mode === this.MODES.h24 && th > 23){
            h.val('23');
            h.data['val'] = 23;
        }
        else if (this.settings.mode === this.MODES.h12 && th > 11){
            h.val('11');
            h.data['val'] = 11;
        }
        else if(th < 0)
        {
            h.val('00');
            h.data['val'] = 0;
        }
        else
        {
            h.val(('0' + th).slice(-2));
            h.data['val'] = th;
        }

        if (isNaN(tm))
        {
            m.val(td[1]);
            m.data['val'] = tdm;
            tm = tdm;
        }
        if (m.val() == '')
        {
            m.val(td[1]);
            m.data['val'] = tdm;
        }
        else if (m.val() > 59){
            m.val('59');
            m.data['val'] = 59;
        }
        else if(m.val() < 0)
        {
            m.val('00');
            m.data['val'] = 0;
        }
        else
        {
            m.val(('0' + tm).slice(-2));
            m.data['val'] = tm;
        }
}

// Validate input value and synchronise with popup values
Plugin.prototype.checkTime = function(e)
{
    if (!this.validTime(this.input.val()))
    {
        this.input.val(this.settings.defaultValue);
    }
    var t = this.input.val().split(':');
    this.tMins.val(('0' + t[1]).slice(-2));
    this.tMins.data['val'] = parseInt(t[1], 10);
    if (this.settings.mode === this.MODES.h24)
    {
        this.tHours.val(('0' + t[0]).slice(-2));
        this.tHours.data['val'] = parseInt(t[0], 10);
        this.input.val(('0' + t[0]).slice(-2) + ':' + ('0' + t[1]).slice(-2));
    }
    else {
        var tt = parseInt(t[0], 10);
        if (tt > 11)
        {
            this.tHours.val('' + tt - 12);
            this.tHours.data['val'] = tt - 12
            this.ampm.text('PM');
        }
        else {
            this.tHours.val(('0' + t[0]).slice(-2));
            this.tHours.data['val'] = tt;
            this.ampm.text('AM');
        }
    }
}

// Check whether time corresponds with time scale
Plugin.prototype.validTime = function(n){
    const cor12 = /^([0-9]|0[0-9]|1[0-1]):([0-9]|[0-5][0-9])$/;
    const cor24 = /^([0-9]|0[0-9]|1[0-9]|2[0-3]):([0-9]|[0-5][0-9])$/;
    if (this.settings.mode === this.MODES.h24)
    {
        if (!cor24.test(n) && n != '')
        {
            return false;
        }
    }
    else {
        if (!cor12.test(n) && n != '')
        {
            return false;
        }
    }
    return true;
}

/** Increment/Decrement -- Limit
* v -> value to be in/decremented
* boolean inc -> specifies whether number should be incremented (true) or decremented (false)
* i -> increment value
* lim -> specifies the limit at which the operation should wrap around
*/
Plugin.prototype.iDL = function(v, inc, i, lim)
{
    if (inc)
    {       // increment
        if (v == lim - 1 || isNaN(v) || v == '')
        {
            return 0;
        }
        else{
            if (i !== null && typeof i !== 'undefined')
            {
                if (parseInt(v) + i > lim - 1)
                {
                    return parseInt(v) + i - lim;
                }
                else {
                    return parseInt(v) + i;
                }
            }
            else{
                return parseInt(v) + 1;
            }
        }
    }
    else{      // decrement
        if (v == 0 || isNaN(v) || v == '')
        {
            return lim - 1;
        }
        else{
            if (i !== null && typeof i !== 'undefined')
            {
                if (parseInt(v) - i < 0)
                {
                    return parseInt(v) - i + lim;
                }
                else {
                    return parseInt(v) - i;
                }
            }
            else{
                return parseInt(v) - 1;
            }
        }
    }

}

// Increment popup hours
Plugin.prototype.incrementHours = function(e){

    if (this.settings.mode === this.MODES.h24)
    {
        this.tHours.val(this.iDL(this.tHours.val(), true, e, 24));
    }
    else {
        this.tHours.val(this.iDL(this.tHours.val(), true, e, 12));
    }
    this.tHours.trigger('change');
};

// Decrement popup hours
Plugin.prototype.decrementHours = function(e){
    if (this.settings.mode === this.MODES.h24)
    {
        this.tHours.val(this.iDL(this.tHours.val(), false, e, 24));
    }
    else {
        this.tHours.val(this.iDL(this.tHours.val(), false, e, 12));
    }
    this.tHours.trigger('change');
};

// Increment popup minutes
Plugin.prototype.incrementMinutes = function(e){
    this.tMins.val(this.iDL(this.tMins.val(), true, e, 60));
    this.tMins.trigger('change');
};

// Decrement popup minutes
Plugin.prototype.decrementMinutes = function(e){
    this.tMins.val(this.iDL(this.tMins.val(), false, e, 60));
    this.tMins.trigger('change');
};

// Setter method for defaultValue
Plugin.prototype.setDefaultValue = function(n)
{
    if (this.validTime(n))
    {
        this.settings.defaultValue = n;
    }
}
// Getter method for default value
Plugin.prototype.getDefaultValue = function()
{
    return this.settings.defaultValue;
}

/** Generic plugin function with instancing functionality
* This method follows the structure of jquery plugins developed for UserFrosting(https://www.userfrosting.com)
* @copyright Alexander Weissman <https://alexanderweissman.com>
*/
$.fn[pluginName] = function(methodOrOptions) {
    // Grab plugin instance
    var instance = $(this).data(pluginName);
    // If undefined or object, initalise plugin.
    if (methodOrOptions === undefined || typeof methodOrOptions === 'object') {
        // Only initalise if not previously done.
        if (!instance) {
            $(this).data(pluginName, new Plugin(this, methodOrOptions));
        }
        return this;
    }
    // Otherwise ensure first parameter is a valid string, and is the name of an actual function.
    else if (typeof methodOrOptions === 'string' && typeof instance[methodOrOptions] === 'function') {
        // Ensure not a private function
        if (methodOrOptions.indexOf('_') !== 0) {
            return instance[methodOrOptions]( Array.prototype.slice.call(arguments, 1));
        }
        else {
            console.warn( 'Method ' +  methodOrOptions + ' is private!' );
        }
    }
    else {
        console.warn( 'Method ' +  methodOrOptions + ' does not exist.' );
    }
};
}( jQuery ));
