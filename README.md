# aiida_experiments
AiiDA experiments on speed increase and space improvements

Space savings
=============
Comments on structure data usage:
- we use structure data because they are a good example. I.e. they are used in calculations (inputs & outputs) and they have various information that are stored as attributes (interesting for our backend comparison)
- the CIF files contain more information than what we store in AiiDA (database) for a structure data object
- an XSF file contains information much closer to what AiIDA stores (in its database) for a structure data object
- the initial idea was to use an XYZ file but the information stored in it was incomplete (maybe the cell coordinates were missing?)

Space comparison among:
- space on disk of the XSF files (convert the provided CIFs to XSFs)
- SQLA database size when loading the XSF files
- Django database size when loading the XSF files

The XSFs will not be stored in the repository when I load them in AiiDA.

Comment from Leopold regarding space calculation
------------------------------------------------
> Spyros:
> I am not sure if the xyz will be stored in the repository when I load them
> in AiiDA. If yes, maybe I should take this space into account.
> With StructureData it shouldn't, so no need to correct for that.

Leopold:
If you were using CifData (which you aren't), you should add the size
of the repository to the size of the DB for the full amount of data
stored by AiiDA.

Spyros: I understand that the same stands for the XSF files loaded as StructureData.


Space saving experiments
------------------------

**Database size calculated by the following command:**
`SELECT pg_size_pretty(pg_database_size('aiidadb_space2_sqla')) As fulldbsize;`
**File size calculated by the following command:**
`du -h .`


> **Small datase experiment (~1000 structure data files) **  
> Django database size: 2045 MB  
> SQLA database size: 45 MB  
> File size: 65  

> **Medium dataset experiment**  
> Dataset: /home/szoupanos/structure_datasets/medium_10k/converted_xsf  
> SQLA DB: aiidadb_space2_sqla  
> Django DB: aiidadb_space2_dj  
>   
> Django database size: 22 GB (22528 MB)  
> SQLA database size: 424 MB  
> File size: 721 MB