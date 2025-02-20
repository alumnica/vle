window.H5PIntegration = {
    "baseUrl": BASE_URL, // No trailing slash
    "url": BASE_URL + H5P_CONTENT,          // Relative to web root
    "postUserStatistics": true,         // Only if user is logged in
    "ajaxPath": "/api/h5p_finished/"+auth_us+"/"+mom+"/",    // Only used by older Content Types
    "ajax": {
        // Where to post user results
        "setFinished": "/api/h5p_finished/"+auth_us+"/"+mom+"/",
        // Words beginning with : are placeholders
        //"contentUserData": "/api/h5p_data/?data_type=:dataType&subContentId=:subContentId"
        "contentUserData": "/api/h5p_data/:subContentId/"
    },
    "saveFreq": false, // How often current content state should be saved. false to disable.
    "user": { // Only if logged in !
        "name": "User Name",
        "mail": "user@mysite.com"
    },
    "siteUrl": "http://www.mysite.com", // Only if NOT logged in!
    "l10n": { // Text string translations
        "H5P": {
            "fullscreen": "Fullscreen",
            "disableFullscreen": "Disable fullscreen",
            "download": "Download",
            "copyrights": "Rights of use",
            "embed": "Embed",
            "size": "Size",
            "showAdvanced": "Show advanced",
            "hideAdvanced": "Hide advanced",
            "advancedHelp": "Include this script on your website if you want dynamic sizing of the embedded content:",
            "copyrightInformation": "Rights of use",
            "close": "Close",
            "title": "Title",
            "author": "Author",
            "year": "Year",
            "source": "Source",
            "license": "License",
            "thumbnail": "Thumbnail",
            "noCopyrights": "No copyright information available for this content.",
            "downloadDescription": "Download this content as a H5P file.",
            "copyrightsDescription": "View copyright information for this content.",
            "embedDescription": "View the embed code for this content.",
            "h5pDescription": "Visit H5P.org to check out more cool content.",
            "contentChanged": "This content has changed since you last used it.",
            "startingOver": "You'll be starting over.",
            "by": "by",
            "showMore": "Show more",
            "showLess": "Show less",
            "subLevel": "Sublevel"
        }
    },
    "loadedJs": [], // Only required when Embed Type = div
    "loadedCss": [],
    "core": { // Only required when Embed Type = iframe
        "scripts": ['jquery.js', 'h5p.js'],
        "styles": ['h5p.css']
    },
    contents: []
};