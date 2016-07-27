$(document).ready(function() {
    $('#sidebar-toggle').click(function() {
        var sidenav = document.getElementsByClassName('SidebarOpen');

        if (sidenav.length > 0) {
            $('body').removeClass("sidebar-open").addClass("sidebar-close");
            $('#left-content').data("state","closed").removeClass("SidebarOpen").addClass("SidebarClose");
            $('#right-content').data("state","closed").removeClass("SidebarOpen").addClass("SidebarClose");
            $('#sidebar-toggle').data("state","closed").removeClass("SidebarOpen").addClass("SidebarClose");
        } else {
            $('body').removeClass("sidebar-close").addClass("sidebar-open");
            $('#left-content').data("state","open").addClass("SidebarOpen").removeClass("SidebarClose");
            $('#right-content').data("state","open").addClass("SidebarOpen").removeClass("SidebarClose");
            $('#sidebar-toggle').data("state","open").addClass("SidebarOpen").removeClass("SidebarClose");
        }
    });
});
