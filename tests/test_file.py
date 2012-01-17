#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Tests.
#
# The Initial Developer of the Original Code is Mozilla.
#
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
#                 Sergey Tupchiy(tupchii.sergii@gmail.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
import pytest
import re
import urllib
from BeautifulSoup import BeautifulSoup

from pages.page_object import MySiteHomePage
from unittestzero import Assert

xfail = pytest.mark.xfail


class TestTemplate():

    ################################################################
    # GENERAL TEST LIST OF MAIN FUNCTIONALITY FOR MARKETING PRODUCTS
    ################################################################
#    def test_that_we_do_something_to_find_a_bug(self, mozwebqa):
#        pass
#
#    def test_header(self, mozwebqa):
#        pass
#
#    def test_footer(self, mozwebqa):
#        pass
#
#    def test_locale(self, mozwebqa):
#        pass

    def test_response_200(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        for url in main_page.get_all_links():
            if '#' in url:
                continue
            response = main_page.get_response_code(url)
            Assert.equal(response, 'The request returned an HTTP 200 response.', 'in url: %s' % url)

    def test_response_404(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        garbage_path = ['/76976cd1a3cbadaf77533a', '/garbage123213', '/blablabla']
        for path in garbage_path:
            url = main_page.base_url + path
            response = main_page.get_response_code(url)
            Assert.equal(response, 'The request returned an HTTP 404 response.', 'in url: %s' % url)
            Assert.true(main_page.is_404_page_present(url))

    def test_validate_links(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        main_page.validate_link(main_page.base_url)

    def test_validate_feeds(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        #feed_link = main_page.get_feed_link
        feed_link = 'http://blog.mozilla.com/feed/'
        validate_result = main_page.validate_feed(feed_link)
        Assert.not_none(validate_result)

    def test_favicon_exist(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        link = main_page.get_favicon_link(main_page.base_url)
        if link:
            match = re.search('favicon.(ico|png|gif)', link)
            if match:
                Assert.contains('favicon', link)
            response = main_page.get_response_code(link)
        elif link == None:
            u = self.urlparse(main_page.base_url)
            link = "%s://%s/favicon.ico" % (u.scheme, u.netloc)
            response = main_page.get_response_code(link)
        else:
            link = '%sfavicon.ico' % main_page.base_url
            response = main_page.get_response_code(link)
        Assert.equal(response, 'The request returned an HTTP 200 response.', 'in url: %s' % link)

    @xfail(reason="not everywhere we have robots :( ")
    def test_robot_txt_present_on_site(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        result = main_page.is_robot_txt_present(main_page.base_url)
        Assert.equal(result, "A robots.txt file is present on the server")
        #TODO: Could be added comparing with proper robots.txt file

#    def test_login(self, mozwebqa):
#        pass
#
#    def test_logout(self, mozwebqa):
#        pass
#
#    def test_create_account(self, mozwebqa):
#        pass
#
#    def test_input_forms_security(self, mozwebqa):
#        pass
#
#    def test_pagination(self, mozwebqa):
#        pass
