#!/bin/sh
echo "\n{literal}\n<script async src='https://www.googletagmanager.com/gtag/js?id=UA-250989682-1'></script>\n<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag('js', new Date());\n\n    gtag('config', 'UA-250989682-1');\n</script>\n{/literal}" >> /var/www/html/themes/classic/templates/_partials/head.tpl
