"""
    Tests for page api
"""

import pytest
import responses

from pyfacebook.exceptions import LibraryError


def test_get_info(helpers, fb_api):
    pid = "20531316728"
    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/{pid}",
            json=helpers.load_json(
                "testdata/facebook/apidata/pages/single_fields_page.json"
            ),
        )

        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}/facebookapp",
            json=helpers.load_json(
                "testdata/facebook/apidata/pages/single_default_page.json"
            ),
        )

        page = fb_api.page.get_info(page_id=pid)
        assert page.id == pid

        page_json = fb_api.page.get_info(
            username="facebookapp",
            fields="id,about,can_checkin,category,category_list,checkins,contact_address,cover,current_location,description,description_html,display_subtext,emails,engagement,fan_count,founded,general_info,global_brand_page_name,global_brand_root_id,link,name,phone,picture,rating_count,single_line_address,start_info,talking_about_count,username,verification_status,website,were_here_count,whatsapp_number",
            return_json=True,
        )
        assert page_json["id"] == pid

    with pytest.raises(LibraryError):
        fb_api.page.get_info()


def test_get_batch(helpers, fb_api):
    page_ids = ["20531316728", "19292868552"]

    with responses.RequestsMock() as m:
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json(
                "testdata/facebook/apidata/pages/multi_default_fields.json"
            ),
        )
        m.add(
            method=responses.GET,
            url=f"https://graph.facebook.com/{fb_api.version}",
            json=helpers.load_json("testdata/facebook/apidata/pages/multi_pages.json"),
        )

        data = fb_api.page.get_batch(ids=page_ids)
        assert page_ids[0] in data.keys()

        data_json = fb_api.page.get_batch(
            ids=page_ids, fields="id,name,username,fan_count", return_json=True
        )
        assert data_json[page_ids[0]]["id"] == page_ids[0]
