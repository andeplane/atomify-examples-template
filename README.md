# Atomify examples template

➡️ **https://andeplane.github.io/atomify?examplesUrl=https://raw.githubusercontent.com/andeplane/atomify-examples-template/main/examples.json**

If you want customize the examples in Atomify for e.g. teaching, you can use this GitHub template (Click the green **Use this template** button in the top of the repository). You can specify simulations and Python notebooks to perform analysis of the simulations.

The configuration is a file ([examples.json](https://github.com/andeplane/atomify-examples-template/blob/main/examples.json)) that you can provide in the Atomify URL. The examples page in Atomify will then show your examples. The format of this file is
```
{
  "baseUrl": "https://raw.githubusercontent.com/andeplane/atomify-examples-template/main",
  "title": "Examples",
  "descriptionFile": "diffusion.md",
  "examples": [
    {
      "id": "diffusion",
      "title": "2D diffusion",
      "description": "We measure the diffusion coefficient",
      "analysisDescription": "This markdown formatted text appears in the default analyze notebook.",
      "imageUrl": "diffusion-2d-msd/diffusion-2d-msd.png",
      "inputScript": "diffusion-2d-msd.in",
      "keywords": [
        "lennard jones",
        "diffusion"
      ],
      "files": [
        {
            "fileName": "diffusion-2d-msd.in",
            "url": "diffusion-2d-msd/diffusion-2d-msd.in"
        },
        {
          "fileName": "diffusion-2d-msd.ipynb",
          "url": "diffusion-2d-msd/diffusion-2d-msd.ipynb"
        }
      ]
    }
  ]
}
```
- `baseUrl` is the prefix of all the file url's. This is typically on the format `https://raw.githubusercontent.com/{user}/{repository}/main`. When you are creating examples locally, you can put `http://localhost:8000` and run `python server.py` to test.
- `title` is the title that appears on top of the examples page in Atomify
- `descriptionFile` is the filename of an (optional) markdown formatted file that appears on top of the examples. Use this to e.g. tell your students what this is about.
- `examples` is an array of the examples.

The examples are on the format
- `id` id of a simulation. This will be used as folder name for both LAMMPS the Jupyter notebook.
- `title` title of the simulation
- `description` description of the simulation
- `analysisDescription (optional)` markdown formatted string that appears in the default analysis notebook
- `imageUrl` url to the image. Full url becomes `{baseUrl}/{imageUrl}`
- `inputScript` file name of the input script
- `keywords` list of keywords that can be used to filter a larger set of simulations
- `files` list of files needed for simulation and analysis. A file is an object with the two properties `fileName` and `url`. Full url becomes `{baseUrl}/{url}`

# Local development
When you are creating a new set of examples, you can point Atomify to a local server. You need to update the `baseUrl` to be `http://localhost:8000` in `examples.json`. Run the server with
```
python server.py
```

and open https://andeplane.github.io/atomify?examplesUrl=http://localhost:8000/examples.json