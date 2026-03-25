# Getting Started — From Manual to Automated with Claude Code + Playwright

This guide takes you from zero to a running Playwright test suite using Claude Code as your AI assistant. You need basic computer skills and curiosity — no prior automation experience required. By the end you'll have 3 working tests you wrote with AI assistance.

---

## 1. Environment Setup

### Python

You need Python 3.10 or higher. Download from [python.org/downloads](https://www.python.org/downloads/) if you don't have it.

Verify your install:
```bash
python --version
# Python 3.12.x  (any 3.10+ is fine)
```

### IDE (Your Code Editor)

Use whichever editor you're comfortable with — Claude Code works from the terminal regardless.

- **VS Code** (free): Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Playwright Test for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright). [Full setup guide](https://code.visualstudio.com/docs/python/python-tutorial).
- **PyCharm Community** (free): Python support built in. [Download here](https://www.jetbrains.com/pycharm/download/). Works out of the box for Python + pytest.

### Playwright + pytest

Open a terminal and run:
```bash
pip install playwright pytest
playwright install chromium
```

- `pip install playwright pytest` — installs the Playwright browser automation library and the pytest test runner
- `playwright install chromium` — downloads a Chromium browser binary that Playwright controls

### Claude Code

Claude Code is Anthropic's CLI tool that brings Claude into your terminal. Install it:

```bash
npm install -g @anthropic-ai/claude-code
```

> **Note:** This requires [Node.js](https://nodejs.org/) — download the LTS version if you don't have it.

Set up your API key:
```bash
claude config set api_key <your-key>
```

Or set the environment variable `ANTHROPIC_API_KEY` in your system.

Launch it to verify:
```bash
claude
```

You should see Claude Code respond and wait for input. See the [official docs](https://docs.anthropic.com/en/docs/claude-code/overview) for detailed setup.

**From here on, we'll use Claude Code for everything.**

---

## 2. Your First Test — Navigate & Assert

**Demo site: [saucedemo.com](https://www.saucedemo.com/)** — a free practice e-commerce site.

Let's start with the simplest possible automation: open a page and check that elements exist. No test framework yet — just a standalone script.

Give Claude Code this prompt:

```
Write a simple Playwright Python script that opens
https://www.saucedemo.com/ and verifies the login page
loads with a username field, password field, and login button.
Don't use pytest — just a standalone script.
```

Claude Code produces something like:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Navigate to the login page
    page.goto("https://www.saucedemo.com/")

    # Verify login page elements exist
    username = page.get_by_placeholder("Username")
    password = page.get_by_placeholder("Password")
    login_btn = page.get_by_role("button", name="Login")

    assert username.is_visible(), "Username field not found"
    assert password.is_visible(), "Password field not found"
    assert login_btn.is_visible(), "Login button not found"

    print("All checks passed — login page loaded correctly!")
    browser.close()
```

**What's happening here:**
- `sync_playwright()` — starts the Playwright engine
- `page.goto()` — navigates to a URL (like typing it in the address bar)
- `get_by_placeholder()` / `get_by_role()` — finds elements on the page by how they appear to users
- `assert` — checks a condition is true, crashes with a message if not
- `headless=False` — shows the browser window so you can watch it work

Run it:
```bash
python my_first_test.py
```

> **You just wrote your first automation test. The prompt was 3 lines.**

---

## 3. Selectors — Finding Elements on the Page

Selectors are the #1 thing to understand. They're how your script finds buttons, fields, text, and links in the HTML. Claude Code picks good selectors automatically, but knowing the options helps you write better prompts and debug failures.

### The 4 Main Approaches

Using SauceDemo as our example:

**1. `get_by_role()` — Accessible role + name (recommended)**
```python
page.get_by_role("button", name="Login")
page.get_by_role("link", name="Twitter")
```
Best for: buttons, links, headings, checkboxes. Matches what screen readers see.

**2. `get_by_text()` — Visible text content**
```python
page.get_by_text("Swag Labs")
page.get_by_text("Sauce Labs Backpack")
```
Best for: labels, headings, product names — any visible text.

**3. `get_by_placeholder()` — Input placeholder text**
```python
page.get_by_placeholder("Username")
page.get_by_placeholder("Password")
```
Best for: form fields with placeholder text.

**4. `page.locator()` — CSS or ID selector (fallback)**
```python
page.locator("#login-button")
page.locator(".inventory_item")
```
Best for: elements without good accessible names or text. Use when the other 3 don't work.

### The Claude Code Angle

When you describe elements in your prompt, be specific about what you *see on screen*. Claude Code translates your description to the right selector strategy.

Try this prompt:
```
The SauceDemo products page has a dropdown to sort products.
It shows "Name (A to Z)" by default. Write a script that
logs in, changes the sort to "Price (low to high)", and
verifies the first product shown is the cheapest ($7.99).
```

Claude Code knows to use `get_by_role("combobox")` for the dropdown and `get_by_role("option")` for the sort choice — because you described what you saw.

---

## 4. Form Filling — A Realistic Interaction

**Demo site: [saucedemo.com](https://www.saucedemo.com/)** — login + add to cart + verify.

Now let's do a real multi-step interaction. Still a standalone script, but this time with form filling, navigation, and dynamic content.

Prompt to Claude Code:
```
Write a Playwright script that:
1. Goes to https://www.saucedemo.com/
2. Logs in with username "standard_user" and password "secret_sauce"
3. Verifies the products page loads with at least 6 items
4. Adds the first product to the cart
5. Goes to the cart and verifies the product is there
```

Claude Code produces:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Step 1: Navigate to login
    page.goto("https://www.saucedemo.com/")

    # Step 2: Log in
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # Step 3: Verify products page
    items = page.locator(".inventory_item")
    assert items.count() >= 6, f"Expected 6+ products, got {items.count()}"
    print(f"Found {items.count()} products")

    # Step 4: Add first product to cart
    page.locator(".inventory_item").first.get_by_role(
        "button", name="Add to cart"
    ).click()

    # Step 5: Go to cart and verify
    page.locator(".shopping_cart_link").click()
    cart_items = page.locator(".cart_item")
    assert cart_items.count() == 1, "Product not in cart"
    print("Product successfully added to cart!")

    browser.close()
```

**Key patterns:**
- `fill()` — types text into an input field (clears it first)
- `click()` — clicks an element (buttons, links, icons)
- `.first` — when multiple elements match, grab the first one
- Chaining: `.first.get_by_role(...)` — find a button *inside* the first product

### When Something Fails

Tests will fail. When they do, paste the error into Claude Code:

```
My test failed with this error:
TimeoutError: page.get_by_role("button", name="Add to cart")
resolved to 6 elements. Strict mode violation.
```

Claude Code reads the error and fixes it — in this case by scoping the selector to the first product. **You don't need to debug Playwright errors yourself.**

---

## 5. Introducing pytest — Why Structure Matters

So far we've written standalone scripts. They work, but they don't scale:
- No shared setup (every script creates its own browser)
- No test reports (just print statements)
- No automatic cleanup when things fail
- Can't run specific tests or groups of tests

**pytest** solves all of this. Let's convert our work.

Prompt to Claude Code:
```
Convert my SauceDemo tests into pytest format. Create:
1. A conftest.py with:
   - A browser fixture (session-scoped, launches once)
   - A page fixture (new page per test)
   - An auto-screenshot fixture that captures on failure
   - Put screenshots in a screenshots/ folder
2. A test file with the login + cart test from before
```

Claude Code produces **conftest.py**:
```python
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOTS = Path(__file__).parent / "screenshots"
SCREENSHOTS.mkdir(exist_ok=True)


@pytest.fixture(scope="session")
def browser():
    """Launch browser once, share across all tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def page(browser, request):
    """Fresh page per test, auto-screenshot on failure."""
    page = browser.new_page()
    yield page

    # Capture screenshot if test failed
    if request.node.rep_call and request.node.rep_call.failed:
        name = request.node.name
        page.screenshot(path=str(SCREENSHOTS / f"FAIL_{name}.png"))

    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the item for the page fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
```

And **test_saucedemo.py**:
```python
def test_login_and_add_to_cart(page):
    # Navigate and log in
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # Verify products loaded
    items = page.locator(".inventory_item")
    assert items.count() >= 6

    # Add first product and verify cart
    items.first.get_by_role("button", name="Add to cart").click()
    page.locator(".shopping_cart_link").click()
    assert page.locator(".cart_item").count() == 1
```

**What changed:**
- **Fixtures** (`browser`, `page`) replace the manual setup/teardown — pytest manages the lifecycle
- **`scope="session"`** on browser means it launches once for the entire test run, not per test
- **Screenshot on failure** happens automatically — no extra code in your tests
- **`yield`** splits a fixture into setup (before yield) and teardown (after yield)

Run it:
```bash
pytest test_saucedemo.py -v -s
```

- `-v` — verbose output (shows each test name and PASSED/FAILED)
- `-s` — shows print statements (useful for debugging)

> **This is the exact same pattern our team uses on real projects.** The `conftest_template.py` in our shared modules is a production version of what Claude Code just generated.

---

## 6. Project Structure — Scaling Beyond One Script

Organize early or drown later. Here's what a clean test project looks like:

```
my_qa_project/
  conftest.py          # shared browser/page fixtures
  screenshots/         # auto-captured on failure
  test_login.py        # login tests
  test_products.py     # product page tests
  test_checkout.py     # checkout flow tests
  helpers/
    selectors.py       # reusable element selectors
    test_data.py       # generated test data
```

### Generated Test Data

Hardcoded test data breaks when you run tests repeatedly (duplicate names, used emails). The `faker` library generates realistic random data every run.

```bash
pip install faker
```

Claude Code prompt:
```
Create a helpers/test_data.py module with functions to
generate random user data: first name, last name, zip code.
Use the Faker library. Then write a checkout test for
SauceDemo that logs in, adds a product, and completes
checkout with the generated data.
```

Claude Code produces **helpers/test_data.py**:
```python
from faker import Faker

fake = Faker()

def generate_checkout_data():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "zip_code": fake.zipcode(),
    }
```

And uses it in the test:
```python
from helpers.test_data import generate_checkout_data

def test_checkout_with_generated_data(page):
    data = generate_checkout_data()

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # Add product and go to cart
    page.locator(".inventory_item").first.get_by_role(
        "button", name="Add to cart"
    ).click()
    page.locator(".shopping_cart_link").click()
    page.get_by_role("button", name="Checkout").click()

    # Fill checkout with generated data
    page.get_by_placeholder("First Name").fill(data["first_name"])
    page.get_by_placeholder("Last Name").fill(data["last_name"])
    page.get_by_placeholder("Zip/Postal Code").fill(data["zip_code"])
    page.get_by_role("button", name="Continue").click()

    # Complete order
    page.get_by_role("button", name="Finish").click()
    assert page.get_by_text("Thank you for your order").is_visible()
```

> **Real projects have shared helpers, generated test data, and conventions docs.** This parallels our project's `data_generators.py` pattern. Start with this structure from day one.

---

## 7. Claude Code + Git — Managing Your Test Code

Claude Code speaks git natively. You don't need to memorize commands — describe what you want in plain English.

```
# Stage and commit your work
"Commit my changes with a message about adding the login and product tests"

# Create a feature branch
"Create a new branch called feature/checkout-tests and switch to it"

# See what changed
"Show me what files I've changed since last commit"

# Undo a mistake
"Discard my changes to conftest.py — I want to go back to the last committed version"
```

### .gitignore

Create a `.gitignore` to keep generated files out of your repo:

```
screenshots/
__pycache__/
.pytest_cache/
*.pyc
```

> **You don't need to memorize git commands.** Describe what you want in plain English and Claude Code translates.

---

## 8. CLAUDE.md — Teaching Claude Code About Your Project

A `CLAUDE.md` file is how you make Claude Code consistently smart about *your* project. It's a markdown file at the root of your project that Claude Code reads automatically every time it starts.

Here's a minimal starter:

```markdown
# My QA Project

## Setup
- Python 3.12, Playwright, pytest
- Run tests: pytest test_*.py -v -s
- Demo site: https://www.saucedemo.com/

## Conventions
- All tests use the shared conftest.py for browser setup
- Screenshots go in screenshots/
- Use Faker for test data generation
- Selectors: prefer get_by_role() over CSS selectors
- Test files: test_<feature>.py

## Test credentials
- SauceDemo: standard_user / secret_sauce
```

**What this gives you:** Every time Claude Code starts a conversation in this folder, it reads this file first. Your conventions become automatic — you don't have to repeat "use the conftest" or "put screenshots in screenshots/" in every prompt.

As your project grows, add patterns, helper function docs, and gotchas you've discovered. See the [Tips & Tricks guide](claudecode_training_tips_and_tricks.md) for advanced CLAUDE.md patterns.

---

## 9. Challenge Exercises

Three graduated exercises using public sites. Try writing the prompts yourself and letting Claude Code generate the code.

### Exercise 1 — Easy: Checkboxes

**Site: [the-internet.herokuapp.com](https://the-internet.herokuapp.com/)**

```
Write a pytest test that:
- Navigates to https://the-internet.herokuapp.com/checkboxes
- Verifies checkbox 1 is unchecked and checkbox 2 is checked
- Clicks checkbox 1 to check it
- Asserts both checkboxes are now checked
```

**What you'll practice:** Basic assertions, checkbox interactions, element state checking.

### Exercise 2 — Medium: Full Checkout Flow

**Site: [saucedemo.com](https://www.saucedemo.com/)**

```
Write a complete checkout flow test using pytest:
- Log in as standard_user / secret_sauce
- Add 3 specific products to the cart by name
- Go to cart and verify all 3 are there
- Complete checkout with Faker-generated user data
- Verify the order confirmation page shows "Thank you for your order"
Include a conftest.py with browser/page fixtures and screenshot on failure.
```

**What you'll practice:** Multi-step flows, generated test data, precise element selection, assertions on dynamic content.

### Exercise 3 — Hard: Mini Test Suite with Structure

**Site: [the-internet.herokuapp.com](https://the-internet.herokuapp.com/)**

```
Create a mini test suite with proper project structure:
- conftest.py with browser/page fixtures + screenshot on failure
- helpers/pages.py with navigation helpers for 3 pages
- test_forms.py — test the login page (/login) with valid and invalid credentials
- test_dynamic.py — test dynamic loading (/dynamic_loading/1): click Start,
  wait for "Hello World!" to appear, assert it's visible
- test_tables.py — test the sortable data tables page (/tables):
  verify the table has data, check a specific cell value
Create a CLAUDE.md for the project.
Ask Claude Code to generate the full structure in one prompt.
```

**What you'll practice:** Project organization, shared fixtures, helper modules, multiple test files, CLAUDE.md conventions — everything a real project needs.

---

## 10. Where to Go Next

- **[Tips & Tricks guide](claudecode_training_tips_and_tricks.md)** — advanced prompting patterns, debugging with Claude Code, shared framework usage
- **[Playwright Python docs](https://playwright.dev/python/)** — full API reference, guides, best practices
- **[Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/overview)** — features, configuration, advanced usage
- **[pytest docs](https://docs.pytest.org/)** — fixtures, markers, plugins, parametrize

> **Your next step:** Pick one manual test you run regularly. Describe it to Claude Code in plain English. Watch it become automated. That's how every test in our project started.