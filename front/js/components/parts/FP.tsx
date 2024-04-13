import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardActionArea from '@mui/material/CardActionArea';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CircularProgress from '@mui/material/CircularProgress';
import { styled } from '@mui/material/styles';
import mammoth from 'mammoth'; // Импорт библиотеки mammoth.js

interface FeaturedPostProps {
    post: {
        description: string;
        title: string;
    };
    onFileUpload: (file: File, fileName: string) => void;
    loading: boolean;
    onButtonClick: () => void;
}

const FeaturedPost: React.FC<FeaturedPostProps> = ({ post, onFileUpload, loading, onButtonClick }) => {
    const [selectedFileName, setSelectedFileName] = useState<string>('');
    const [preview, setPreview] = useState<string>(''); // Состояние для превью

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setSelectedFileName(file.name);
            onFileUpload(file, file.name); 
    
            try {
                // Используем mammoth для конвертации .doc/.docx в HTML
                const result = await mammoth.convertToHtml({ arrayBuffer: file });
                 // Ограничиваем превью первыми 200 словами
                 const previewText = result.value.split(' ').slice(0, 40).join(' ');
                 setPreview(previewText); // Обновляем состояние с превью
            } catch (error) {
                console.error('Error converting file:', error);
                // Обработка ошибок при конвертации
                setPreview('Ошибка при конвертации файла');
            }
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
                        {/* Показываем превью */}
                        <div dangerouslySetInnerHTML={{ __html: preview }} />

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
            {loading && <CircularProgress />} 
        </Grid>
    );
}

export default FeaturedPost;