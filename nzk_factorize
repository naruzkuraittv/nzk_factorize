import requests
import re

# Function to extract all `showid` links from the HTML
def extract_showid_link(html_text, n=-1, verbosity="silent") -> int:
    links = []
    for line in html_text.splitlines():
        if '(show)' in line:  # We look for lines with 'showid='
            start = line.find('showid=') + len('showid=')
            end = line.find('">(show)', start)
            showid = line[start:end]
            if showid.isdigit():  # Ensure it's a numeric ID
                links.append(showid)
    links = list(dict.fromkeys([x for x in links if x != ""]))
    
    if not links:  # Handle empty lists
        status_factor = status(request(n))
        if status_factor == "Prime":
            if verbosity != "silent":
                print("number is prime")
        for line in html_text.splitlines():
            if 'id=' in line:  # We look for lines with 'showid='
                start = line.find('id=') + len('id=')
                end = line.find('">(show)', start)
                showid = line[start:end]
                if showid.isdigit():  # Ensure it's a numeric ID
                    links.append(showid)
            links = list(dict.fromkeys([x for x in links if x != ""]))

    if len(links) > 1:
        print(f"Multiple showid links found: {links}, returning 0th of list")
        return int(links[0])
    
    # Convert to int
    return int(links[0])

def extract_number_from_page(showid, verbosity="silent") -> int:
    number_url = f"https://factordb.com/index.php?showid={showid}"
    number_response = requests.get(number_url).text
    numbers = []
    collect = False
    
    for line in number_response.splitlines():
        if 'Number' in line:  # This starts where the number begins
            collect = True
            continue
        # If we are in the section with the number, collect the number parts
        if collect:
            clean_line = line.replace("<br>", "").strip()  # Clean the line by removing <br>
            if clean_line.endswith("</td>"):
                clean_line = clean_line[:-5]  # Remove trailing </td>
            # Append only digits
            numbers.append(''.join(filter(str.isdigit, clean_line)))
            if '</td>' in line:  # This ends the collection
                break

    # Join all the extracted number parts into one string
    number_number = ''.join(numbers)
    if not number_number:  # If no number was found, handle it
        if verbosity != "silent":
            print("No number found on the page.")
        return None  # Return None if no valid number was found
    
    if verbosity != "silent":
        print(f"number found: {number_number}")
    
    # Convert the cleaned number to int and return it
    return int(number_number)

# Function to find all links on a page
def function_find_all_links(input_html: str, filter_link: str) -> list:
    # Use regex to find all href links of the form `index.php?id=anynumber`
    links = re.findall(r'index\.php\?id=\d+', input_html)
    
    # Remove duplicates by converting to a set and back to a list
    links = list(set(links))
    
    # Remove the `filter_link` (i.e., n_show_link) if it exists in the links
    filter_link = f'index.php?id={filter_link}'
    if filter_link in links:
        links.remove(filter_link)
    
    # Strip index.php?id= from each entry
    links = [x.replace('index.php?id=', '') for x in links]
    
    # If no links are found, return the filter link
    if links == []:
        links.append(filter_link) # we hate life
    return links

# function to find all prime numbers of a page
def function_to_find_all_primes_of_a_page(input_html: str, verbosity="silent", input_number=-1) -> list:
    result_links = function_find_all_links(input_html, extract_showid_link(input_html))
    n = input_number
    primes = []
    
    # print the extracted links if verbosity is not silent
    if verbosity != "silent":
        print("id for each prime: ", result_links)
    
    # extract the number from each entry from the result_link
    for entry in result_links:
        prime = extract_number_from_page(entry)
        if prime is None:
            if verbosity != "silent":
                 print("number is prime")
            return [ n , 1 ] # we hate life
        if verbosity != "silent":
            print("Prime number: ", prime) 
        primes.append(prime)
    
    return primes # we love life

def status(input) -> str:
    gettype = type(input)
    if gettype == int:
        # Convert to string before querying
        response = request(str(input))
    elif gettype == str:
        if "<title>factordb.com</title>" in input:
            response = input
        else:
            response = request(input)
    else:
        return "we hate life, input is invalid", gettype
    
    if "<td>C</td>" in response or "<td>C </td>" in response or "<td> C </td>" in response or "<td> C</td>" in response:
        return "Composite, no factors known"
    elif "<td>CF</td>" in response or "<td>CF </td>" in response or "<td> CF </td>" in response or "<td> CF</td>" in response:
        return "Composite, factors known"
    elif "<td>FF</td>" in response or "<td>FF </td>" in response or "<td> FF </td>" in response or "<td> FF</td>" in response:
        return "Composite, fully factored"
    elif "<td>P</td>" in response or "<td>P </td>" in response or "<td> P </td>" in response or "<td> P</td>" in response:
        return "Prime"
    elif "<td>U</td>" in response or "<td>U </td>" in response or "<td> U </td>" in response or "<td> U</td>" in response:
        return "Unknown"
    elif "<td>Prp</td>" in response or "<td>Prp </td>" in response or "<td> Prp </td>" in response or "<td> Prp</td>" in response:
        return "Probably prime"
    elif "<td>Unit</td>" in response or "<td>Unit </td>" in response or "<td> Unit </td>" in response or "<td> Unit</td>" in response:
        return "Just for 1"
    elif "<td>N</td>" in response or "<td>N </td>" in response or "<td> N </td>" in response or "<td> N</td>" in response:
        return "This number is not in database (and was not added due to your settings)"
    else:  # we hate life
        return "we hate life something went wrong in response: " + response

# combined function to use the functions so we can call this one instead of doing this over and over again so when we turn this into a py repo it just works

def query(input: str) -> str:
    query = f"https://factordb.com/index.php?query={input}"
    response = requests.get(query).text
    return response
def request(input: str) -> str:
    return query(input)

def factors(n: str, verbosity="silent", mode="list" ) -> list:
    # generate the query URL for the given number `n`
    # then fetch the FactorDB page for the composite number
    response = request(n)
    status_factor = status(response)
    if status_factor == "Prime":
        if verbosity != "silent":
            print("number is prime")
        return [n, 1]
    else:
        list_of_primes = function_to_find_all_primes_of_a_page(response, verbosity, n)
        #sort list by size biggest first

        if mode == "list":
            return list_of_primes
        else:
            list_of_primes.sort(reverse=True)
            p = list_of_primes[0]
            q = list_of_primes[1]
            return p, q

#future idea, command that does
# if 'Composite, factors known' and only list length is 2 try list[0] and if thats cf and also listoflistzero[0] is = list[0] report 'composit, not completely factored' idk maybe its not needed
