<h1>Steam-API-Analyzer</h1>
<p>Steam-API-Analyzer is a data analysis project built with <strong>Python</strong>, <strong>pandas</strong> and the <strong>Steam Web API</strong>. The goal of the project is to retrieve my own Steam library, analyze how I actually spend my time in games, enrich the data with game genres and present the results as charts and an interactive dashboard.</p>
<p>This project was created as a portfolio application to practice data analysis in Python, working with REST APIs, data cleaning and transformation with pandas, and data visualization.</p>
<hr />
<h2>Project Status</h2>
<p>The project is currently in development.</p>
<p>Already working:</p>
<ul>
<li>Fetching the full list of owned games from the Steam Web API</li>
<li>API key and SteamID kept in a <code>.env</code> file, outside the repository</li>
<li>Converting the API response into a pandas DataFrame</li>
<li>Playtime converted to hours and last played time converted to dates</li>
<li>Top 10 most played games</li>
<li>Count and share of never launched games</li>
<li>Games not launched for the longest time, with days since last launch</li>
</ul>
<p>Still planned:</p>
<ul>
<li>Game genres from the Steam Store API</li>
<li>Charts with matplotlib and seaborn</li>
<li>Caching API results to a local file</li>
<li>Interactive dashboard in Streamlit</li>
</ul>
<hr />
<h2>Main Features</h2>
<h3>Library Overview</h3>
<p>Fetches all games owned by the account, including titles, using the <code>IPlayerService/GetOwnedGames</code> endpoint with <code>include_appinfo=1</code>.</p>
<h3>Playtime Analysis</h3>
<p>Statistics:</p>
<ul>
<li>total playtime converted to hours</li>
<li>top 10 most played games</li>
<li>games not launched for the longest time, with days since last launch</li>
</ul>
<h3>Pile of Shame</h3>
<p>Shows how many owned games have never been launched and what share of the library they make up.</p>
<h3>Genres</h3>
<p>Planned: genres for each game will be retrieved from the Steam Store API and joined with the library data, which allows:</p>
<ul>
<li>total playtime per genre</li>
<li>most common genres in the library</li>
<li>genres with the highest share of unplayed games</li>
</ul>
<h3>Dashboard</h3>
<p>Planned Streamlit dashboard with:</p>
<ul>
<li>library summary (number of games, total hours, unplayed share)</li>
<li>most played games chart</li>
<li>playtime by genre chart</li>
<li>filtering by genre and playtime</li>
</ul>
<hr />
<h2>Tech Stack</h2>
<ul>
<li><strong>Language:</strong> Python 3.13+, Jupyter Notebooks</li>
<li><strong>Data:</strong> pandas, matplotlib, seaborn</li>
<li><strong>API:</strong> requests, python-dotenv</li>
<li><strong>Tooling:</strong> uv, Ruff, mypy, nbstripout</li>
<li><strong>Dashboard:</strong> Streamlit (planned)</li>
</ul>
<hr />
<h2>Running Locally</h2>
<p>Requirements: <a href="https://docs.astral.sh/uv/">uv</a> and a Steam account.</p>
<h3>1. Install dependencies</h3>
<pre><code class="language-bash">git clone https://github.com/nszolc/Steam-API-Analyzer.git
cd Steam-API-Analyzer
uv sync
</code></pre>
<p><code>uv sync</code> creates the virtual environment in <code>.venv</code> and installs the exact package versions from <code>uv.lock</code>.</p>
<h3>2. Get your Steam credentials</h3>
<ul>
<li><strong>API key</strong>: generate one at <a href="https://steamcommunity.com/dev/apikey">https://steamcommunity.com/dev/apikey</a> (any domain name works, e.g. <code>localhost</code>).</li>
<li><strong>SteamID64</strong>: the 17-digit account ID, visible in the profile URL or on sites like steamid.io.</li>
<li><strong>Privacy settings</strong>: in <em>Profile → Edit Profile → Privacy Settings</em>, set <em>Game details</em> to <strong>Public</strong>.</li>
</ul>
<h3>3. Configure the environment</h3>
<p>Copy <code>.env.example</code> to <code>.env</code> and fill in your values:</p>
<pre><code>STEAM_API_KEY=your_api_key
STEAM_ID=your_steamid64
</code></pre>
<h3>4. Run the notebook</h3>
<p>Open the notebook in VS Code (select the <code>.venv</code> kernel), or start Jupyter from the project root:</p>
<pre><code class="language-bash">uv run jupyter lab
</code></pre>
<p>The notebook only handles analysis; the API code lives in the <code>steam_api_analyzer</code> package, so it can be reused later by the dashboard:</p>
<pre><code class="language-python">from steam_api_analyzer import get_owned_games

games = get_owned_games()
</code></pre>
<p>Two details worth knowing:</p>
<ul>
<li><code>load_dotenv()</code> looks for <code>.env</code> starting from the current working directory, so Jupyter should be started from the project root.</li>
<li>If <em>Game details</em> are private, the API still returns <code>200 OK</code>, but with an empty <code>response</code> object, so <code>fetch_owned_games()</code> checks for a missing <code>games</code> list and raises a clear error instead of failing later.</li>
</ul>
<hr />
<h2>Configuration</h2>
<p>Unlike a local database password, a Steam API key is a real credential tied to the account, so it is kept out of the repository from the very first commit. The <code>.env</code> file is gitignored, and <code>.env.example</code> documents the required variables without values.</p>
<p>Notebook outputs can contain personal data as well (SteamID, raw API responses), so <a href="https://github.com/kynan/nbstripout">nbstripout</a> is configured as a git filter in <code>.gitattributes</code> and strips cell outputs on commit. After cloning, enable it once with:</p>
<pre><code class="language-bash">uv run nbstripout --install
</code></pre>
<hr />
<h2>Data Source</h2>
<h3>Steam Web API</h3>
<p>Endpoint: <code>IPlayerService/GetOwnedGames/v1/</code></p>
<p>Fields used in the analysis:</p>
<pre><code>appid               - unique game identifier
name                - game title
playtime_forever    - total playtime (in minutes)
rtime_last_played   - last launch time (Unix timestamp)
</code></pre>
<h3>Steam Store API</h3>
<p>Planned: <code>store.steampowered.com/api/appdetails</code> for genres. This endpoint is undocumented and rate-limited, which is the main reason for caching its results locally instead of calling it on every run.</p>
<hr />
<h2>Project Structure</h2>
<pre><code>Steam-API-Analyzer
│
├── src
│   └── steam_api_analyzer
│       ├── __init__.py
│       └── api.py             (Steam Web API client)
├── notebooks
│   └── steam_analysis.ipynb   (data analysis)
├── data                       (cached API results, gitignored - planned)
├── .env.example               (required environment variables)
├── .gitattributes             (nbstripout filter for notebooks)
├── pyproject.toml             (project, dependencies, Ruff and mypy config)
└── uv.lock                    (locked dependency versions)
</code></pre>
<hr />
<h2>Roadmap</h2>
<h3>Version 1 - Library Analysis</h3>
<ul>
<li>☑ Fetch owned games from the Steam Web API</li>
<li>☑ Store credentials in <code>.env</code></li>
<li>☑ Convert playtime to hours</li>
<li>☑ Top 10 most played games</li>
<li>☑ Count and share of never launched games</li>
<li>☑ Games not launched for the longest time</li>
</ul>
<h3>Version 2 - Genres and Charts</h3>
<ul>
<li>☑ Fetch genres from the Steam Store API</li>
<li>☐ Cache API results to a local file</li>
<li>☐ Merge genres with library data</li>
<li>☐ Playtime statistics by genre</li>
<li>☐ Charts with matplotlib and seaborn</li>
</ul>
<h3>Version 3 - Dashboard</h3>
<ul>
<li>☐ Build a Streamlit dashboard</li>
<li>☐ Add filters by genre and playtime</li>
<li>☐ Add library summary metrics</li>
</ul>
<h3>Version 4 - Extra Features</h3>
<ul>
<li>☐ Store data in a local SQLite database</li>
<li>☐ Analyze achievements with <code>ISteamUserStats/GetPlayerAchievements</code></li>
<li>☐ Track playtime changes over time</li>
</ul>
<hr />
<h2>Data Notice</h2>
<p>Game data is provided by Valve Corporation via the Steam Web API. This project is not affiliated with Valve.</p>
<hr />
<h2>Author</h2>
<p>Created by Natalia Szolc as a data analysis portfolio project.</p>
<p>GitHub: <a href="https://github.com/nszolc">github.com/nszolc</a>
Portfolio: <a href="https://nszolc.dev">nszolc.dev</a></p>
