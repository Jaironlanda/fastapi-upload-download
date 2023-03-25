from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

# from .db.models import Team, User
from .db.config import get_session
from .db.utils import create_upload, get_upload, get_list_file
from .db.schemas import FileDataBase

# from .db.schemas import TeamBase, User, UserBase, TeamWithUser, Team, UserCreate
import base64
import io


router = APIRouter(prefix="/api/v1")


@router.post("/", tags=["Upload"])
async def upload_file(file: UploadFile, session: AsyncSession = Depends(get_session)):

    contents = await file.read()
    upload_path = "upload/{}".format(file.filename)
    file_base64 = base64.b64encode(contents)

    # upload to server
    with open(upload_path, "wb+") as f:
        f.write(contents)

    return await create_upload(
        {
            "owner_id": 1,
            "filename": file.filename,
            "filepath": upload_path,
            "filebase64": file_base64
        }
        , session=session)
    

@router.get("/list", tags=['List File'])
async def list_file(session: AsyncSession = Depends(get_session), limit: Optional[int] = 10,
    skip: Optional[int] = 0,):
    return await get_list_file(session, skip=skip, limit=limit)

@router.get("/d1", tags=["Download"])
async def download_file_1(id: str, session: AsyncSession = Depends(get_session)):
    
    myfile = await get_upload(id, session=session)
    print(myfile)
    
    return FileResponse(
        path=myfile['filepath'],
        filename=myfile['filename']
    )

@router.get("/d2", tags=["Download"])
async def download_file_2(id: str, session: AsyncSession = Depends(get_session)):
   
   result = await get_upload(id, session=session)
   decode_file = base64.b64decode(result['filebase64'])

   file_like = io.BytesIO(decode_file)
   
   headers = {
        "Content-Disposition": f"attachment; filename=newfile.png"
    }
   
   return Response(
       content=file_like.getvalue(), media_type="application/octet-stream", headers=headers
   )
