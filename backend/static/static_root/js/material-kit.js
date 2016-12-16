var transparent = true;

var transparentDemo = true;
var fixedTop = false;

var navbar_initialized = false;

$(document).ready(function(){

    // Init Material scripts for buttons ripples, inputs animations etc, more info on the next link https://github.com/FezVrasta/bootstrap-material-design#materialjs
    $.material.init();

    //  Activate the Tooltips
    $('[data-toggle="tooltip"], [rel="tooltip"]').tooltip();

    // Activate Datepicker
    if($('.datepicker').length != 0){
        $('.datepicker').datepicker({
             weekStart:1
        });
    }

    // Check if we have the class "navbar-color-on-scroll" then add the function to remove the class "navbar-transparent" so it will transform to a plain color.
    if($('.navbar-color-on-scroll').length != 0){
        $(window).on('scroll', materialKit.checkScrollForTransparentNavbar)
    }

    // Activate Popovers
    $('[data-toggle="popover"]').popover();

    // Active Carousel
	$('.carousel').carousel({
      interval: 400000
    });

});

materialKit = {
    misc:{
        navbar_menu_visible: 0
    },

    checkScrollForTransparentNavbar: debounce(function() {
            if($(document).scrollTop() > 260 ) {
                if(transparent) {
                    transparent = false;
                    $('.navbar-color-on-scroll').removeClass('navbar-transparent');
                }
            } else {
                if( !transparent ) {
                    transparent = true;
                    $('.navbar-color-on-scroll').addClass('navbar-transparent');
                }
            }
    }, 17),

    initSliders: function(){
        // Sliders for demo purpose
        $('#sliderRegular').noUiSlider({
            start: 40,
            connect: "lower",
            range: {
                min: 0,
                max: 100
            }
        });

        $('#sliderDouble').noUiSlider({
            start: [20, 60] ,
            connect: true,
            range: {
                min: 0,
                max: 100
            }
        });
    }
}


var big_image;

materialKitDemo = {
    checkScrollForParallax: debounce(function(){
        var current_scroll = $(this).scrollTop();

        oVal = ($(window).scrollTop() / 3);
        big_image.css({
            'transform':'translate3d(0,' + oVal +'px,0)',
            '-webkit-transform':'translate3d(0,' + oVal +'px,0)',
            '-ms-transform':'translate3d(0,' + oVal +'px,0)',
            '-o-transform':'translate3d(0,' + oVal +'px,0)'
        });

    }, 6)

}
// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		clearTimeout(timeout);
		timeout = setTimeout(function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		}, wait);
		if (immediate && !timeout) func.apply(context, args);
	};
};

// Profile Builder Page

$(document).ready(function () {
    //Initialize tooltips
    $('.nav-tabs > li a[title]').tooltip();
    
    //Wizard
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {

        var $target = $(e.target);
    
        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);

    });
    $(".prev-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        prevTab($active);

    });
});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}

// Prepare the preview for profile picture
$("#wizard-picture").change(function(){
    readURL(this);
});
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Tags

(function($) {

    var delimiter = new Array();
    var tags_callbacks = new Array();
    $.fn.doAutosize = function(o){
        var minWidth = $(this).data('minwidth'),
            maxWidth = $(this).data('maxwidth'),
            val = '',
            input = $(this),
            testSubject = $('#'+$(this).data('tester_id'));

        if (val === (val = input.val())) {return;}

        // Enter new content into testSubject
        var escaped = val.replace(/&/g, '&amp;').replace(/\s/g,' ').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        testSubject.html(escaped);
        // Calculate new width + whether to change
        var testerWidth = testSubject.width(),
            newWidth = (testerWidth + o.comfortZone) >= minWidth ? testerWidth + o.comfortZone : minWidth,
            currentWidth = input.width(),
            isValidWidthChange = (newWidth < currentWidth && newWidth >= minWidth)
                                 || (newWidth > minWidth && newWidth < maxWidth);

        // Animate width
        if (isValidWidthChange) {
            input.width(newWidth);
        }


  };
  $.fn.resetAutosize = function(options){
    // alert(JSON.stringify(options));
    var minWidth =  $(this).data('minwidth') || options.minInputWidth || $(this).width(),
        maxWidth = $(this).data('maxwidth') || options.maxInputWidth || ($(this).closest('.tagsinput').width() - options.inputPadding),
        val = '',
        input = $(this),
        testSubject = $('<tester/>').css({
            position: 'absolute',
            top: -9999,
            left: -9999,
            width: 'auto',
            fontSize: input.css('fontSize'),
            fontFamily: input.css('fontFamily'),
            fontWeight: input.css('fontWeight'),
            letterSpacing: input.css('letterSpacing'),
            whiteSpace: 'nowrap'
        }),
        testerId = $(this).attr('id')+'_autosize_tester';
    if(! $('#'+testerId).length > 0){
      testSubject.attr('id', testerId);
      testSubject.appendTo('body');
    }

    input.data('minwidth', minWidth);
    input.data('maxwidth', maxWidth);
    input.data('tester_id', testerId);
    input.css('width', minWidth);
  };

    $.fn.addTag = function(value,options) {
            options = jQuery.extend({focus:false,callback:true},options);
            this.each(function() {
                var id = $(this).attr('id');

                var tagslist = $(this).val().split(delimiter[id]);
                if (tagslist[0] == '') {
                    tagslist = new Array();
                }

                value = jQuery.trim(value);

                if (options.unique) {
                    var skipTag = $(this).tagExist(value);
                    if(skipTag == true) {
                        //Marks fake input as not_valid to let styling it
                        $('#'+id+'_tag').addClass('not_valid');
                    }
                } else {
                    var skipTag = false;
                }

                if (value !='' && skipTag != true) {
                    $('<span>').addClass('tag label label-info').append(
                        $('<span>').text(value).append('&nbsp;&nbsp;'),
                        $('<a>', {
                            href  : '#',
                            title : 'Removing tag',
                            text  : 'x'
                        }).click(function () {
                            return $('#' + id).removeTag(escape(value));
                        })
                    ).insertBefore('#' + id + '_addTag');

                    tagslist.push(value);

                    $('#'+id+'_tag').val('');
                    if (options.focus) {
                        $('#'+id+'_tag').focus();
                    } else {
                        $('#'+id+'_tag').blur();
                    }

                    $.fn.tagsInput.updateTagsField(this,tagslist);

                    if (options.callback && tags_callbacks[id] && tags_callbacks[id]['onAddTag']) {
                        var f = tags_callbacks[id]['onAddTag'];
                        f.call(this, value);
                    }
                    if(tags_callbacks[id] && tags_callbacks[id]['onChange'])
                    {
                        var i = tagslist.length;
                        var f = tags_callbacks[id]['onChange'];
                        f.call(this, $(this), tagslist[i-1]);
                    }
                }

            });

            return false;
        };

    $.fn.removeTag = function(value) {
            value = unescape(value);
            this.each(function() {
                var id = $(this).attr('id');

                var old = $(this).val().split(delimiter[id]);

                $('#'+id+'_tagsinput .tag').remove();
                str = '';
                for (i=0; i< old.length; i++) {
                    if (old[i]!=value) {
                        str = str + delimiter[id] +old[i];
                    }
                }

                $.fn.tagsInput.importTags(this,str);

                if (tags_callbacks[id] && tags_callbacks[id]['onRemoveTag']) {
                    var f = tags_callbacks[id]['onRemoveTag'];
                    f.call(this, value);
                }
            });

            return false;
        };

    $.fn.tagExist = function(val) {
        var id = $(this).attr('id');
        var tagslist = $(this).val().split(delimiter[id]);
        return (jQuery.inArray(val, tagslist) >= 0); //true when tag exists, false when not
    };

    // clear all existing tags and import new ones from a string
    $.fn.importTags = function(str) {
                id = $(this).attr('id');
        $('#'+id+'_tagsinput .tag').remove();
        $.fn.tagsInput.importTags(this,str);
    }

    $.fn.tagsInput = function(options) {
    var settings = jQuery.extend({
      interactive:true,
      defaultText:'Type and enter skills',
      minChars:0,
      width:'300px',
      height:'100px',
      autocomplete: {selectFirst: false },
      'hide':true,
      'delimiter':',',
      'unique':true,
      removeWithBackspace:true,
      placeholderColor:'#666666',
      placeholderWidth:'145',
      autosize: true,
      comfortZone: 20,
      inputPadding: 6*2
    },options);

        this.each(function() {
            if (settings.hide) {
                $(this).hide();
            }
            var id = $(this).attr('id');
            if (!id || delimiter[$(this).attr('id')]) {
                id = $(this).attr('id', 'tags' + new Date().getTime()).attr('id');
            }

            var data = jQuery.extend({
                pid:id,
                real_input: '#'+id,
                holder: '#'+id+'_tagsinput',
                input_wrapper: '#'+id+'_addTag',
                fake_input: '#'+id+'_tag'
            },settings);

            delimiter[id] = data.delimiter;

            if (settings.onAddTag || settings.onRemoveTag || settings.onChange) {
                tags_callbacks[id] = new Array();
                tags_callbacks[id]['onAddTag'] = settings.onAddTag;
                tags_callbacks[id]['onRemoveTag'] = settings.onRemoveTag;
                tags_callbacks[id]['onChange'] = settings.onChange;
            }

            var markup = '<div id="'+id+'_tagsinput" class="tagsinput"><div id="'+id+'_addTag">';

            if (settings.interactive) {
                markup = markup + '<input id="'+id+'_tag" value="" data-default="'+settings.defaultText+'" />';
            }

            markup = markup + '</div><div class="tags_clear"></div></div>';

            $(markup).insertAfter(this);

            $(data.holder).css('width',settings.width);
            $(data.holder).css('min-height',settings.height);
    
            if ($(data.real_input).val()!='') {
                $.fn.tagsInput.importTags($(data.real_input),$(data.real_input).val());
            }
            if (settings.interactive) {
                $(data.fake_input).val($(data.fake_input).attr('data-default'));
                $(data.fake_input).css('color',settings.placeholderColor);
                $(data.fake_input).css('width',settings.placeholderWidth);
                $(data.fake_input).resetAutosize(settings);

                $(data.holder).bind('click',data,function(event) {
                    $(event.data.fake_input).focus();
                });

                $(data.fake_input).bind('focus',data,function(event) {
                    if ($(event.data.fake_input).val()==$(event.data.fake_input).attr('data-default')) {
                        $(event.data.fake_input).val('');
                    }
                    $(event.data.fake_input).css('color','#000000');
                });

                if (settings.autocomplete_url != undefined) {
                    autocomplete_options = {source: settings.autocomplete_url};
                    for (attrname in settings.autocomplete) {
                        autocomplete_options[attrname] = settings.autocomplete[attrname];
                    }

                    if (jQuery.Autocompleter !== undefined) {
                        $(data.fake_input).autocomplete(settings.autocomplete_url, settings.autocomplete);
                        $(data.fake_input).bind('result',data,function(event,data,formatted) {
                            if (data) {
                                $('#'+id).addTag(data[0] + "",{focus:true,unique:(settings.unique)});
                            }
                        });
                    } else if (jQuery.ui.autocomplete !== undefined) {
                        $(data.fake_input).autocomplete(autocomplete_options);
                        $(data.fake_input).bind('autocompleteselect',data,function(event,ui) {
                            $(event.data.real_input).addTag(ui.item.value,{focus:true,unique:(settings.unique)});
                            return false;
                        });
                    }


                } else {
                        // if a user tabs out of the field, create a new tag
                        // this is only available if autocomplete is not used.
                        $(data.fake_input).bind('blur',data,function(event) {
                            var d = $(this).attr('data-default');
                            if ($(event.data.fake_input).val()!='' && $(event.data.fake_input).val()!=d) {
                                if( (event.data.minChars <= $(event.data.fake_input).val().length) && (!event.data.maxChars || (event.data.maxChars >= $(event.data.fake_input).val().length)) )
                                    $(event.data.real_input).addTag($(event.data.fake_input).val(),{focus:true,unique:(settings.unique)});
                            } else {
                                $(event.data.fake_input).val($(event.data.fake_input).attr('data-default'));
                                $(event.data.fake_input).css('color',settings.placeholderColor);
                            }
                            return false;
                        });

                }
                // if user types a comma, create a new tag
                $(data.fake_input).bind('keypress',data,function(event) {
                    if (event.which==event.data.delimiter.charCodeAt(0) || event.which==13 ) {
                        event.preventDefault();
                        if( (event.data.minChars <= $(event.data.fake_input).val().length) && (!event.data.maxChars || (event.data.maxChars >= $(event.data.fake_input).val().length)) )
                            $(event.data.real_input).addTag($(event.data.fake_input).val(),{focus:true,unique:(settings.unique)});
                        $(event.data.fake_input).resetAutosize(settings);
                        return false;
                    } else if (event.data.autosize) {
                        $(event.data.fake_input).doAutosize(settings);

                    }
                });
                //Delete last tag on backspace
                data.removeWithBackspace && $(data.fake_input).bind('keydown', function(event)
                {
                    if(event.keyCode == 8 && $(this).val() == '')
                    {
                         event.preventDefault();
                         var last_tag = $(this).closest('.tagsinput').find('.tag:last').text();
                         var id = $(this).attr('id').replace(/_tag$/, '');
                         last_tag = last_tag.replace(/[\s]+x$/, '');
                         $('#' + id).removeTag(escape(last_tag));
                         $(this).trigger('focus');
                    }
                });
                $(data.fake_input).blur();

                //Removes the not_valid class when user changes the value of the fake input
                if(data.unique) {
                    $(data.fake_input).keydown(function(event){
                        if(event.keyCode == 8 || String.fromCharCode(event.which).match(/\w+|[Ã¡Ã©Ã­Ã³ÃºÃÃ‰ÃÃ“ÃšÃ±Ã‘,/]+/)) {
                            $(this).removeClass('not_valid');
                        }
                    });
                }
            } // if settings.interactive
        });

        return this;

    };

    $.fn.tagsInput.updateTagsField = function(obj,tagslist) {
        var id = $(obj).attr('id');
        $(obj).val(tagslist.join(delimiter[id]));
    };

    $.fn.tagsInput.importTags = function(obj,val) {
        $(obj).val('');
        var id = $(obj).attr('id');
        var tags = val.split(delimiter[id]);
        for (i=0; i<tags.length; i++) {
            $(obj).addTag(tags[i],{focus:false,callback:false});
        }
        if(tags_callbacks[id] && tags_callbacks[id]['onChange'])
        {
            var f = tags_callbacks[id]['onChange'];
            f.call(obj, obj, tags[i]);
        }
    };

})(jQuery);

// Save Buttons
$('.saving').on('click', function() {
    var $this = $(this);
  $this.button('loading');
    setTimeout(function() {
       $this.button('reset');
   }, 8000);
});

// Profile meter
