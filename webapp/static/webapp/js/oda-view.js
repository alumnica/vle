
$(document).ready(function () {
    $('#fullpage').fullpage({
        anchors: ['firstPage', 'secondPage', '3rdPage', '4thPage', '5thPage', '6thPage'],
        // sectionsColor: ['#C63D0F', '#1BBC9B', '#7E8F7C'],
        navigation: true,
        navigationPosition: 'left',
        // navigationTooltips: ['First page', 'Second page', 'Third and last page'],
        paddingBottom: '3rem',
        paddingTop: '3rem',
        verticalCentered: false,
        menu: '#menu',
        onLeave: function (origin, destination, direction) {
            var leavingSection = this;
            var indState = $('.indication').css('display');

            if (origin == 1 && indState == 'none') {
                $('.indication').fadeIn(1500);
            }
            else if (origin == 2 && direction == 'up') {
                $('.indication').fadeOut(500);
            }
        }
    });


    $('.section[state]').each(function () {
        var state = $(this).attr('state'),
            theId = $(this).attr('menu-ref');
        theRef = '.e' + theId;
        if (state == 'complete') {
            $(theRef).toggleClass(theRef).toggleClass('s' + theId);
        }
    });

    var w = window,
        d = document,
        e = d.documentElement,
        g = d.getElementsByTagName('body')[0],
        x = w.innerWidth || e.clientWidth || g.clientWidth,
        y = w.innerHeight || e.clientHeight || g.clientHeight;

    fileLoader(x);

    window.addEventListener("orientationchange", function () {
        var w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0],
            x = w.innerWidth || e.clientWidth || g.clientWidth,
            y = w.innerHeight || e.clientHeight || g.clientHeight;

        fileLoader(y);

    });


});

function fileLoader(x) {

    var activ = document.getElementById('activ'),
        apli = document.getElementById('apli'),
        ejemp = document.getElementById('ejemp'),
        forma = document.getElementById('forma'),
        sens = document.getElementById('sens');

    var activMp4H = '/static/webapp/media/uODAs/activ/activ_m_h.mp4',
        activWebmH = '/static/webapp/media/uODAs/activ/activ_m_h.webm',
        activPngH = '/static/webapp/media/uODAs/activ/activ_m_h.png',
        activMp4V = '/static/webapp/media/uODAs/activ/activ_m_v.mp4',
        activWebmV = '/static/webapp/media/uODAs/activ/activ_m_v.webm',
        activPngV = '/static/webapp/media/uODAs/activ/activ_m_v.png',

        apliMp4H = '/static/webapp/media/uODAs/apli/apli_m_h.mp4',
        apliWebmH = '/static/webapp/media/uODAs/apli/apli_m_h.webm',
        apliPngH = '/static/webapp/media/uODAs/apli/apli_m_h.png',
        apliMp4V = '/static/webapp/media/uODAs/apli/apli_m_v.mp4',
        apliWebmV = '/static/webapp/media/uODAs/apli/apli_m_v.webm',
        apliPngV = '/static/webapp/media/uODAs/apli/apli_m_v.png',

        ejempMp4H = '/static/webapp/media/uODAs/ejemp/ejemp_m_h.mp4',
        ejempWebmH = '/static/webapp/media/uODAs/ejemp/ejemp_m_h.webm',
        ejempPngH = '/static/webapp/media/uODAs/ejemp/ejemp_m_h.png',
        ejempMp4V = '/static/webapp/media/uODAs/ejemp/ejemp_m_v.mp4',
        ejempWebmV = '/static/webapp/media/uODAs/ejemp/ejemp_m_v.webm',
        ejempPngV = '/static/webapp/media/uODAs/ejemp/ejemp_m_v.png',

        formaMp4H = '/static/webapp/media/uODAs/forma/forma_m_h.mp4',
        formaWebmH = '/static/webapp/media/uODAs/forma/forma_m_h.webm',
        formaPngH = '/static/webapp/media/uODAs/forma/forma_m_h.png',
        formaMp4V = '/static/webapp/media/uODAs/forma/forma_m_v.mp4',
        formaWebmV = '/static/webapp/media/uODAs/forma/forma_m_v.webm',
        formaPngV = '/static/webapp/media/uODAs/forma/forma_m_v.png',

        sensMp4H = '/static/webapp/media/uODAs/sens/sens_m_h.mp4',
        sensWebmH = '/static/webapp/media/uODAs/sens/sens_m_h.webm',
        sensPngH = '/static/webapp/media/uODAs/sens/sens_m_h.png',
        sensMp4V = '/static/webapp/media/uODAs/sens/sens_m_v.mp4',
        sensWebmV = '/static/webapp/media/uODAs/sens/sens_m_v.webm',
        sensPngV = '/static/webapp/media/uODAs/sens/sens_m_v.png';


    if (x > 1000) {
        //desktop

    } else if (x > 450) {
        //mobile landscape    
        $('#activ .mp4').attr('src', activMp4H);
        $('#activ .webm').attr('src', activWebmH);
        $('#activ .png').attr('src', activPngH);
        activ.load();
        activ.play();

        $('#apli .mp4').attr('src', apliMp4H);
        $('#apli .webm').attr('src', apliWebmH);
        $('#apli .png').attr('src', apliPngH);
        apli.load();
        apli.play();

        $('#ejemp .mp4').attr('src', ejempMp4H);
        $('#ejemp .webm').attr('src', ejempWebmH);
        $('#ejemp .png').attr('src', ejempPngH);
        ejemp.load();
        ejemp.play();

        $('#forma .mp4').attr('src', formaMp4H);
        $('#forma .webm').attr('src', formaWebmH);
        $('#forma .png').attr('src', formaPngH);
        forma.load();
        forma.play();

        $('#sens .mp4').attr('src', sensMp4H);
        $('#sens .webm').attr('src', sensWebmH);
        $('#sens .png').attr('src', sensPngH);
        sens.load();
        sens.play();
    } else if (x < 450) {
        //mobile portrait
        $('#activ .mp4').attr('src', activMp4V);
        $('#activ .webm').attr('src', activWebmV);
        $('#activ .png').attr('src', activPngV);
        activ.load();
        activ.play();

        $('#apli .mp4').attr('src', apliMp4V);
        $('#apli .webm').attr('src', apliWebmV);
        $('#apli .png').attr('src', apliPngV);
        apli.load();
        apli.play();

        $('#ejemp .mp4').attr('src', ejempMp4V);
        $('#ejemp .webm').attr('src', ejempWebmV);
        $('#ejemp .png').attr('src', ejempPngV);
        ejemp.load();
        ejemp.play();

        $('#forma .mp4').attr('src', formaMp4V);
        $('#forma .webm').attr('src', formaWebmV);
        $('#forma .png').attr('src', formaPngV);
        forma.load();
        forma.play();

        $('#sens .mp4').attr('src', sensMp4V);
        $('#sens .webm').attr('src', sensWebmV);
        $('#sens .png').attr('src', sensPngV);
        sens.load();
        sens.play();
    }
}
