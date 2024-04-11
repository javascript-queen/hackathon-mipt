import axios from 'axios';
import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardActionArea from '@mui/material/CardActionArea';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { styled } from '@mui/material/styles';

// В интерфейсе FeaturedPostProps добавим поле для имени файла
interface FeaturedPostProps {
    post: {
        description: string;
        title: string;
    };
    onFileUpload: (file: File, fileName: string) => void; // Функция для передачи выбранного файла и его имени в родительский компонент
}

// В компоненте FeaturedPost передаем имя файла вместе с файлом при вызове onFileUpload
const FeaturedPost: React.FC<FeaturedPostProps> = ({ post, onFileUpload }) => {
    const [selectedFileName, setSelectedFileName] = useState<string>('');

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setSelectedFileName(file.name);
            onFileUpload(file, file.name); // Теперь передаем и имя файла, и сам файл
        }
    };

    const VisuallyHiddenInput = styled('input')({
        clip: 'rect(0 0 0 0)',
        clipPath: 'inset(50%)',
        height: 1,
        overflow: 'hidden',
        position: 'absolute',
        bottom: 0,
        left: 0,
        whiteSpace: 'nowrap',
        width: 1,
    });

    return (
        <Grid item xs={12} md={6}>
            <CardActionArea component="a" href="#">
                <Card sx={{ display: 'flex' }}>
                    <CardContent sx={{ flex: 1 }}>
                        <Typography component="h2" variant="h5">
                            {post.title}
                        </Typography>
                        <Typography variant="subtitle1" paragraph>
                            {post.description}
                        </Typography>
                        <Button
                            component="label"
                            role={undefined}
                            variant="contained"
                            tabIndex={-1}
                            startIcon={<CloudUploadIcon />}
                        >
                            {selectedFileName ? selectedFileName : "Загрузить файл"}
                            <VisuallyHiddenInput type="file" accept=".doc, .docx" onChange={handleFileChange} />
                        </Button>
                    </CardContent>
                </Card>
            </CardActionArea>
        </Grid>
    );
}

export default FeaturedPost;
