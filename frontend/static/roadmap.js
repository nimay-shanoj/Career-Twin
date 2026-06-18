function generateRoadmap(){

    let career =
    document.getElementById("career").value;

    let roadmap =
    document.getElementById("roadmap");

    if(career=="Select Goal"){
        alert("Please select a career goal");
        return;
    }

    roadmap.style.display="block";

    if(career=="Backend Developer"){

        roadmap.innerHTML =

        `
        <h2>Backend Developer Roadmap</h2>

        1. Learn Python <br><br>

        2. Learn SQL & MySQL <br><br>

        3. Learn Flask <br><br>

        4. Learn Django <br><br>

        5. Learn Git & GitHub <br><br>

        6. Build Backend Projects
        `;
    }

    else if(career=="Python Developer"){

        roadmap.innerHTML =

        `
        <h2>Python Developer Roadmap</h2>

        1. Python Basics <br><br>

        2. OOP Concepts <br><br>

        3. File Handling <br><br>

        4. MySQL <br><br>

        5. Flask/Django <br><br>

        6. Projects
        `;
    }

    else if(career=="Full Stack Developer"){

        roadmap.innerHTML =

        `
        <h2>Full Stack Roadmap</h2>

        1. HTML <br><br>

        2. CSS <br><br>

        3. JavaScript <br><br>

        4. Python <br><br>

        5. Django <br><br>

        6. Full Stack Projects
        `;
    }

    else{

        roadmap.innerHTML =

        `
        <h2>Data Analyst Roadmap</h2>

        1. Python <br><br>

        2. Excel <br><br>

        3. SQL <br><br>

        4. Pandas <br><br>

        5. Power BI <br><br>

        6. Analytics Projects
        `;
    }

}