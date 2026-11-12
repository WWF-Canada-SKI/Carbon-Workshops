# Publish the Blue Carbon theme

This branch contains the Blue Carbon Eelgrass Workshop and its Jekyll theme. The four workshop parts keep their existing paths.

For a separate, shareable preview while the full workshop library stays online, push this branch to a dedicated GitHub repository. In that repository open **Settings → Pages**, select **Deploy from a branch**, choose the branch and **/(root)**, and save. GitHub Pages supplies the repository base path.

To use this branch as the site for `CathalD/Carbon-Workshops`, select `blue-carbon-jekyll` and **/(root)** in the same Pages settings. This makes Blue Carbon the published site for that repository and replaces its current full workshop library at that address.

Once Pages reports a successful deployment, open **Visit site**. Navigate to the workshop part you want to share and copy its address. The Part 4 path after the site base is `Blue%20Carbon%20Workshops/04_Results/`.

To preview locally with the GitHub Pages gem installed, run `jekyll serve` from the branch root.
