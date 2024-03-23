community_list = {"Local Jewish Community Centers (JCCs)": "https://jcca.org/jccs/",
                  "Anti-Defamation League (ADL) Community Programs" : "https://www.adl.org/contact-us",
                  "Europeans fight Antisemitism": "https://www.facebook.com/groups/1058554350876592/",
                  "JewishGen Communities Database": "https://www.jewishgen.org/communities/search.asp",
                  "Meetup": "https://www.meetup.com/find/?keywords=jewish%20community&source=EVENTS&location=israel"
                  }

def print_resources():
    resources = ""
    for key, value in community_list.items():
         resources += f"Resource: {key} \nurl: {value}\n"
         resources += "------------------\n"
    return resources

