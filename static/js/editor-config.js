CKEDITOR.plugins.addExternal('confighelper', '/static/extra plugin/confighelper/', 'plugin.js');

CKEDITOR.editorConfig = function( config ) {
    config.extraPlugins= 'codesnippet,confighelper';
    config.removePlugins = 'resize';
    config.language = 'fa';
    config.toolbar = [
       ['Bold','Italic','Underline','StrikeThrough'],
       ['NumberedList','BulletedList','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
        ['Link','Image', 'CodeSnippet']
    ] ;
    config.contentsCss = ['/static/css/base.css'];
    config.skin = 'moono-lisa,/static/extra plugin/moono-lisa/';
    config.placeholder = 'sss';


};

