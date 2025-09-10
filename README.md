# For Users
The website as accessible through https://emsolution-ssil.github.io/EMOptSolutionDoc/.

# For Developers
## 1. Initial Setup
1. Install [Node.js](https://nodejs.org/en/download/) (LTS version recommended).
    ```bash
    node -v
    ```
2. Clone the repository to your local machine.
    ```bash   
    git clone xxx
    ```
3. Navigate to the cloned directory in your terminal.
    ```bash
    cd EMOptSolutionDoc
    ```
4. Install the dependencies 
    ```bash
    npm install
    ```

## 2. Running the Development Server
```bash
npm run start
```

## 3. Deploying the Documentation
```bash
$env:GIT_USER="<Your GitHub username>"
npm run deploy
```
This will build the documentation and deploy it to the `gh-pages` branch of your repository. It might take a few minutes for the changes to be reflected on the live site.
